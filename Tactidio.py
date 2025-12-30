import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from tkvideo import tkvideo
from PIL import Image,ImageDraw,ImageFont,ImageTk
from time import sleep
import textwrap as tw
import csv
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import threading
import pyttsx3
import requests
from langchain_ollama import OllamaLLM
from ollama import chat
from langchain_core.prompts import ChatPromptTemplate
import pytesseract as pyt
import os
import cv2
import imutils
import shutil
from deep_translator import GoogleTranslator
sound_lock=threading.Lock()
sound_enabled=True
a=0
t=0
l=0
i=0
h=0
transkey = {
    "English": "en", "Spanish": "es", "French": "fr",
    "German": "de", "Chinese (Simplified)": "zh-CN", "Chinese   (Traditional)": "zh-TW",
    "Japanese": "ja", "Korean": "ko", "Russian": "ru",
    "Italian": "it", "Portuguese": "pt", "Arabic": "ar",
    "Dutch": "nl", "Turkish": "tr", "Hindi": "hi",
    "Swedish": "sv", "Danish": "da", "Norwegian": "no",
    "Finnish": "fi", "Greek": "el", "Hebrew": "he",
    "Indonesian": "id", "Polish": "pl", "Romanian": "ro",
    "Thai": "th", "Hungarian": "hu", "Czech": "cs",
    "Catalan": "ca", "Slovak": "sk", "Ukrainian": "uk",
    "Croatian": "hr", "Malay": "ms", "Vietnamese": "vi",
    "Serbian": "sr", "Bulgarian": "bg", "Lithuanian": "lt",
    "Slovenian": "sl", "Latvian": "lv", "Estonian": "et",
    "Maltese": "mt", "Icelandic": "is", "Irish": "ga",
    "Macedonian": "mk", "Albanian": "sq", "Welsh": "cy",
    "Basque": "eu", "Galician": "gl", "Belarusian": "be",
    "Swahili": "sw", "Yiddish": "yi", "Afrikaans": "af",
    "Breton": "br", "Scottish Gaelic": "gd", "Armenian": "hy",
    "Azerbaijani": "az", "Georgian": "ka", "Luxembourgish": "lb",
    "Uzbek": "uz", "Bosnian": "bs", "Esperanto": "eo",
    "Javanese": "jv", "Latin": "la", "Maori": "mi",
    "Mongolian": "mn", "Punjabi": "pa", "Tamil": "ta",
    "Telugu": "te", "Urdu": "ur", "Yoruba": "yo",
    "Zulu": "zu", "Filipino": "tl", "Cebuano": "ceb",
    "Hmong": "hmn", "Khmer": "km", "Lao": "lo",
    "Myanmar (Burmese)": "my", "Nepali": "ne", "Sinhala": "si",
    "Tajik": "tg", "Amharic": "am","Select Language": "en"
}
root=ctk.CTk()
width=root.winfo_screenwidth()
height=root.winfo_screenheight()
root.geometry("%dx%d" % (width,height))
root.title("Braille Converter")
webcam_ip = "192.0.0.4:8080"
menubarcolour="#25b8cf"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Relative paths for assets
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
IMAGES_DIR = os.path.join(RESOURCES_DIR, "images")
FONTS_DIR = os.path.join(RESOURCES_DIR, "fonts")
DATA_DIR = os.path.join(RESOURCES_DIR, "data")
VIDEOS_DIR = os.path.join(RESOURCES_DIR, "videos")
# Dynamic path for Tesseract (finds it in system PATH)
TESSERACT_PATH = shutil.which("tesseract")
if not TESSERACT_PATH:
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

s_index=0
running=True
# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
rate=engine.setProperty("rate",150)
#This is the plan the model follows when answering prompts
'''template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
"""'''
#model = OllamaLLM(model="llama3")
#prompt = ChatPromptTemplate.from_template(template)
#chain = prompt | model
def translate(text2,lang1):
    translated = GoogleTranslator(source="en", target=lang1).translate(text2)
    return translated
def speak(text):
    with sound_lock:  # Acquire lock for thread-safe access
        if sound_enabled and not engine._inLoop:
            engine.say(text)
            engine.runAndWait()
txt=" "
#The AI function has 
'''def get_response(prompt):
    global a
    if a==0:
        context=""
        speak("Welcome to the AI ChatBot !")

        #Context is basically the chat history or referring to a previous prompt in the current prompt
        result = chain.invoke({"context": "", "question": prompt})
        speak(result)
        context+= f"\nUser: {prompt}\nAI: {result}"'''

def changetheme(command):
    x = command.lower().replace("theme is", "").strip()
    global menubarcolour
    menubarcolour=x
    theme(themes[menubarcolour])

#icons
toggleicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "toggle_btn_icon.png"))
homeicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "home_icon.png"))
audioicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "audio_icon.png"))
texticon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "text_icon.png"))
imageicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "image_icon.png"))
servicesicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "services_icon.png"))
def switchindication(indicatorlabel,page):

    homebuttonindicator.config(bg=menubarcolour)
    audiobuttonindicator.config(bg=menubarcolour)
    textbuttonindicator.config(bg=menubarcolour)
    imagebuttonindicator.config(bg=menubarcolour)
    servicesbuttonindicator.config(bg=menubarcolour)
    indicatorlabel.config(bg="red")

    if menubarframe.winfo_width()>55:
        foldmenubar()
    for frame in pageframe.winfo_children():
        frame.destroy()
    page()
closebuttonicon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "close_btn_icon.png"))

def extend_menu_bar():
    menubarframe.config(width=200)
    togglemenubutton.config(image=closebuttonicon)
    togglemenubutton.config(command=foldmenubar)

def foldmenubar():
    menubarframe.config(width=55)
    togglemenubutton.config(image=toggleicon)
    togglemenubutton.config(command=extend_menu_bar)

def homepage():
    global s_index
    s_index=0
    s="     This app is brought to you by : Official Sponsor - Avraneel Ghosh , Principal Partner - Khushi Rai , and Primary Associate - Asmii Shripad"
    global a,h,t,l,i
    h=1
    if h==1 and a==0 and t==0 and l==0 and i==0:
        def listenforcommandhome():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                while a==0:
                    speak("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        speak(f"You said: {command}")
                        processcommandhome(command)  # Process the recognized command
                        h=0
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

    def processcommandhome(command):
        global h
        # Here you can define how to handle different commands
        command = command.lower()
        if "what is your name" in command:
            speak("I am Nirvana, your voice assistant.")
        elif "how are you" in command:
            speak("I am just a program, but thanks for asking!")

        elif "current time" in command:
            currenttime=datetime.now().strftime("%H:%M")
            currentdate=datetime.now().strftime("%A, %B %d, %Y")
            speak(f"The current time is: {currenttime} and today is {currentdate}")
        
        elif "go to" in command:
            
            if "text converter" in command:
                for frame in pageframe.winfo_children():
                    frame.destroy()
                h=0
                textpage()
            elif "audio converter" in command:
                for frame in pageframe.winfo_children():
                    frame.destroy()
                h=0
                audiopage()
            elif "image converter" in command:
                for frame in pageframe.winfo_children():
                    frame.destroy()
                h=0
                imagepage()
            elif "home" in command:
                for frame in pageframe.winfo_children():
                    frame.destroy()
                h=0
                homepage()
            elif "help page" in command:
                for frame in pageframe.winfo_children():
                    frame.destroy()
                h=0
                helppage()
        elif "theme is" in command:
            changetheme(command)

        elif "exit" in command :
            speak("Goodbye!")
            root.quit()  # Close the Tkinter app

        elif "no sound" in command:
            global sound_enabled
            sound_enabled=False
        else:
            print(command)
            pass

    def update():
        global s_index
        double = s + "  " + s               # double string so slicing wraps around
        display = double[s_index:s_index+120]# get display slice

        s_index += 1                        # shift next display one left
        if s_index >= len(double) // 2:     # reset index if near end of text
            s_index = 0
        now=datetime.now()

        currentdate=now.strftime("%d-%m-%y")
        currenttime=now.strftime("%H:%M:%S")
        
        string="    ",currentdate,"                                                                  ",display,"                                                                  ",currenttime," "
        string1 = "".join(str(l) for l in list(string))
        label1.configure(text=string1)
        statusbar.after(1000, update)     # reschedule function

    statusbar=ctk.CTkFrame(pageframe)
    statusbar.pack(side="top",fill="x")
    statusbar.configure(bg_color="black",height=50)

    label1=ctk.CTkLabel(statusbar,text="",font=("Arial",15))
    label1.place(y=10,x=10)

    update()
    homepageframe=tk.Frame(pageframe)
    Bg1=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "bg1.png"))
    Bg2=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "bg2.png"))
    
    homeframe=ctk.CTkScrollableFrame(homepageframe,width=width,height=1700,
                                    label_anchor="center",)
    homeframe.pack(pady=0,fill="both",expand=True)
    
    # Create a bg label 1
    backgroundlabel1 = ctk.CTkLabel(homeframe, text="", image=Bg1)
    backgroundlabel1.pack(pady=0)

    # Create a bg label 2
    backgroundlabel2 = ctk.CTkLabel(homeframe, text="", image=Bg2)
    backgroundlabel2.pack(pady=0)

    textlabel3=ctk.CTkLabel(homeframe, text=
    """
    Braille Converter   
    By: Avraneel, Khushi, Asmii   
    """,font=("Arial",50))
    textlabel3.place(x=750,y=1005,anchor="center")

    # Create a txt label 2
    textlabel2=ctk.CTkLabel(homeframe, text=
    """
    Braille is a system of touch reading and writing for blind persons in which 
    raised dots represent the letters of the alphabet.  
    It also contains equivalents for punctuation marks and provides symbols to show letter groupings.
    People read braille by moving the hand or hands from left to right along each line.
    The reading process usually involves both hands, and the index fingers generally do the reading.

    
    The history of braille goes all the way back to the early 1800s. 
    A man named Charles Barbier who served in Napoleon Bonaparte’s French army developed a unique 
    system known as “night writing” so soldiers could communicate safely during the night. 
    As a military veteran, Barbier saw several soldiers killed because they used lamps after dark 
    to read combat messages. As a result of the light shining from the lamps, enemy combatants 
    knew where the French soldiers were and inevitably led to the loss of many men.

    
    At eleven years old, Braille found inspiration to modify Charles Barbier’s “night writing” 
    code in an effort to create an efficient written communication system for fellow blind individuals. 
    He enrolled at the National Institute of the Blind in Paris one year earlier. 
    He spent the better part of the next nine years developing and refining the system of raised 
    dots that we now know by his name, Braille. 

    
    After all of Braille’s work, the code was now based on cells with only 6-dots or with 8-dots 
    instead of 12 . This crucial improvement meant that a fingertip could 
    encompass the entire cell unit with one impression and Stop rapidly from one cell to the next. 
    Over time, the world gradually accepted braille as the fundamental form of written communication 
    for blind individuals. Today it remains basically as he invented it. 
    """,font=("Arial",24),bg_color="transparent")
    textlabel2.place(x=750,y=1155,anchor="n")
    textlabel2.configure(bg_color="transparent")

    homepageframe.pack(fill=tk.BOTH, expand=True)
    h=0
    # Start the listening thread
    threading.Thread(target=listenforcommandhome, daemon=True).start()

def textpage():
    global transkey
    global menubarcolour
    global a,l,i,t,h
    t=1
    if t==1 and a==0 and l==0 and i==0 and h==0:
        def listenforcommandtext():  
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                while a==0:
                    speak("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        speak(f"You said: {command}")
                        processcommandtext(command)  # Process the recognized command
                        t=0
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        def processcommandtext(command):
            global t
            # Here you can define how to handle different commands
            command = command.lower()
            if "what is your name" in command:
                speak("I am Nirvana, your voice assistant.")
            
            elif "go to" in command:
                if "text converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    t=0
                    textpage()
                elif "audio converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    t=0
                    audiopage()
                elif "image converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    t=0
                    imagepage()
                elif "home" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    t=0
                    homepage()
                elif "help page" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    t=0
                    helppage()
            elif "theme is" in command:
                changetheme(command)

            elif "exit" in command :
                speak("Goodbye!")
                root.quit()  # Close the Tkinter app

            elif "no sound" in command:
                global sound_enabled
                sound_enabled=False
            elif "submit" in command:
                if "text" in command:
                    print("HI")
                    texttobraille(transkey[lang1.get()])
                elif "braille" in command or "other" in command:
                    brailletotext(transkey[lang1.get()])
            elif "help" in command or "ai overview" in command or "eye overview" in command or "ai" in command:
                aioverview()
            
            elif "text" in command:
                textinput.focus_set()
            elif "braille" in command or "other" in command or "brain" in command:
                brailleinput.focus_set()
            else:
                print(command)
                pass

        def texttobraille(lang):
            text = textinput.get("0.0", "end").lower()
            text = text.strip()
            x = translate(text, lang)
            brailledict = {
                "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛",
                "h": "⠓", "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝",
                "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞", "u": "⠥",
                "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",
                "1": "⠼⠁", "2": "⠼⠃", "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋",
                "7": "⠼⠛", "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚",
                " ": "   ", ".": "⠲", ",": "⠂", "?": "⠦", "!": "⠖", ":": "⠾", ";": "⠆",
                """: "⠄", "-": "⠤", "/": "⠌", "(": "⠷", ")": "⠾", """: "⠶", "\n": "\n"
            }
            brailletext = "".join(brailledict.get(char, "") for char in x)
            brailleoutput.configure(text=brailletext)

        def brailletotext(lang):
            text = brailleinput.get("0.0", "end").lower()
            text = text.strip()
            englishdict = {
                "⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e", "⠋": "f", "⠛": "g",
                "⠓": "h", "⠊": "i", "⠚": "j", "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n",
                "⠕": "o", "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s", "⠞": "t", "⠥": "u",
                "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y", "⠵": "z",
                "⠼⠁": "1", "⠼⠃": "2", "⠼⠉": "3", "⠼⠙": "4", "⠼⠑": "5", "⠼⠋": "6",
                "⠼⠛": "7", "⠼⠓": "8", "⠼⠊": "9", "⠼⠚": "0",
                " ": " ", "⠲": ".", "⠂": ",", "⠦": "?", "⠖": "!", "⠾": ":", "⠆": ";",
                "⠄": """, "⠤": "-", "⠌": "/", "⠷": "(", "⠾": ")", "⠶": """, "\n": "\n"
            }
            englishtext = "".join(englishdict.get(char, "") for char in text)
            x = translate(englishtext, lang)
            brailleoutput.configure(text=x)

        def aioverview():

            inputtext = textinput.get("0.0", "end").strip()
            outputtext = brailleoutput.cget("text").strip()
            if inputtext:
                explaintext = inputtext
            elif outputtext:
                explaintext = outputtext
            else:
                explaintext = ""
            if explaintext:
                try:
                    messages = [
                        {'role': 'system', 'content': 'Be concise and precise. Reply in max 6-7 continuous sentences and include only essential details and use only alphabetic characters. Avoid using punctuation marks like commas, periods, or quotation marks.'},
                        {'role': 'user', 'content': explaintext},
                    ]
                    response = chat('deepseek-v3.1:671b-cloud', messages=messages, options={'temperature': 0.2, 'max_tokens': 120})
                    speak(response['message']['content'])

                except Exception as e:
                    tk.messagebox.showerror("AI Overview Error", str(e))

        textpageframe = ctk.CTkFrame(pageframe)
        textpageframe.pack(pady=0, fill="both", expand=True)

        textframe = ctk.CTkScrollableFrame(textpageframe, width=width, height=1700, label_anchor="center", )
        textframe.pack(pady=0, fill="both", expand=True)

        label1 = tk.Label(textframe, width=1900, height=1000)
        label1.pack()
        vid1 = tkvideo(os.path.join(VIDEOS_DIR, "text_video(1).mp4"), label1, loop=1, size=(1900, 1000))
        vid1.play()

        textinput = ctk.CTkTextbox(textframe, height=150,
                                width=500, font=("Helvetica", 18), wrap="word", corner_radius=50, text_color="black",
                                fg_color=menubarcolour)
        textinput.place(x=100, y=150, anchor="nw")

        def submit2():
            texttobraille(transkey[lang1.get()])

        submittext = ctk.CTkButton(textframe, text="Submit text", command=submit2, corner_radius=50, bg_color="transparent",
                                fg_color=menubarcolour, text_color="black")
        submittext.place(x=100, y=350, anchor="sw")

        brailleinput = ctk.CTkTextbox(textframe, height=150,
                                    width=500, font=("Helvetica", 18), wrap="word", corner_radius=50, text_color="black",
                                    fg_color=menubarcolour)
        brailleinput.place(x=100, y=400, anchor="nw")

        lang1 = tk.StringVar()
        lang1.set("Select Language")

        options = ctk.CTkOptionMenu(textframe, variable=lang1, values=list(transkey.keys()),
                                    corner_radius=50, fg_color=menubarcolour, text_color="black")
        options.place(x=400, y=600, anchor="sw")

        def submit1():
            brailletotext(transkey[lang1.get()])

        submitbraille = ctk.CTkButton(textframe, text="Submit braille", command=submit1, corner_radius=50, bg_color="transparent",
                                    fg_color=menubarcolour, text_color="black")
        submitbraille.place(x=100, y=600, anchor="sw")

        brailleoutput = ctk.CTkLabel(textframe, text="", width=600, height=500,
                                    corner_radius=50, justify="left",
                                    fg_color=menubarcolour, bg_color="transparent",
                                    text_color="black", font=("Arial", 20))
        brailleoutput.place(x=800, y=150, anchor="nw")
        aibutton = ctk.CTkButton(
            textpageframe,
            text="AI Overview",
            command=aioverview,
            corner_radius=50,
            fg_color=menubarcolour,
            text_color="black",
            font=("Arial", 18)
        )
        aibutton.place(x=1400,y=50,anchor="ne")

        textpageframe.pack(fill=tk.BOTH, expand=True)
        t=0
        # Start the listening thread
        threading.Thread(target=listenforcommandtext, daemon=True).start()

def audiopage():
    global t,l,a,i,h
    global menubarcolour
    braillealphabet = {
        "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
                    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
                    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
                    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
                    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽",
                    "z": "⠵", " ": " ", "\n":"\n", "1":"⠼⠁", "2":"⠼⠃",
                    "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛",
                    "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚", ",": "⠂", ";": "⠆",
                    ":": "⠒", ".": "⠲", "?": "⠦", "!": "⠖", """: "⠄", "|":"⠖",
                    """: "⠄⠶", "(": "⠐⠣", ")": "⠐⠜", "/": "⠸⠌", "-": "⠤",
                    "_": "⠐⠠⠤", "<":" ", ">":" ", "{":" ", "}":" ","@":" ",
                    "#":" ", "$":" ", "%":" ", "^":" ", "&":" ", "*":" ", "+":" ",
                    "=":" ", "“":"⠘⠦", "”":"⠘⠴", "‘":"⠄⠦", "’":"⠄⠴", "–":"⠠⠤", "—":"⠐⠠⠤",
                    "©":" ", "°":" ", "÷":" ", "¡":" ", "¿":" ", "®":" ",
                    "~":" ", "™":" ", "«":" ", "»":" ", "€":" ", "¢":" ","\\":" ", "[":" ",
                    "]":" ", "é":" ", "§":" ", "¥":" ", "£":" ", "₨":" ", "₹":" ", "₩":" ",
                    "₺":" ", "₼":" ","₽":" ", "₿":" ", "₼":" "
    }
    a=1
    if a==1 and h==0 and t==0 and l==0 and i==0:
        def listenforcommandaudio():
            global a
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                while a==0:
                    speak("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        speak(f"You said: {command}")
                        processcommandaudio(command)  # Process the recognized command
                        a=0
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        def processcommandaudio(command):
            global a
            # Here you can define how to handle different commands
            command = command.lower()
            if "what is your name" in command:
                speak("I am Nirvana, your voice assistant.")
            
            elif "go to" in command:
                
                if "text converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    a=0
                    textpage()
                elif "audio converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    a=0
                    audiopage()
                elif "image converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    a=0
                    imagepage()
                elif "home" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    a=0
                    homepage()
                elif "help page" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    a=0
                    helppage()
            elif "theme is" in command:
                changetheme(command)

            elif "exit" in command :
                speak("Goodbye!")
                root.quit()  # Close the Tkinter app

            elif "no sound" in command:
                
                global sound_enabled
                sound_enabled=False
            elif "submit" in command:
                if "audio input" in command:
                    listenforsound(transkey[lang1.get()])
                elif "audio file" in command:
                    recogniseaudiofile(transkey[lang1.get()])
                elif "braille" in command or "other" in command:
                    brailletoaudio(transkey[lang1.get()])
            elif "help" in command or "ai overview" in command or "eye overview" in command or "ai" in command:
                aioverview()
            elif "audio input" in command:
                audioinput.focus_set()
            elif "braille" in command or "other" in command or "brain" in command:
                brailleinput.focus_set()
            elif "audio file" in command or "audio" in command:
                audiodirectory.focus_set()

            else:
                print(command)
                pass

        def audiotobraille(text1):
            x=""
            a=0
            for i in range(len(text1)):
                if a<21:
                    x+=(braillealphabet.get(text1[i].lower(),"?"))
                    a+=1
                else:
                    x+="\n"
                    a=0
            brailleoutput.configure(text=x)

        def brailletoaudio(lang="en"):
            englishtranslation=""
            text=brailleinput.get("0.0","end").lower()
            text=text.strip()
            print(text)
            englishdict = {
                "⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e", "⠋": "f", "⠛": "g",
                "⠓": "h", "⠊": "i", "⠚": "j", "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n",
                "⠕": "o", "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s", "⠞": "t", "⠥": "u",
                "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y", "⠵": "z",
                "⠼⠁": "1", "⠼⠃": "2", "⠼⠉": "3", "⠼⠙": "4", "⠼⠑": "5", "⠼⠋": "6",
                "⠼⠛": "7", "⠼⠓": "8", "⠼⠊": "9", "⠼⠚": "0",
                " ": " ", "⠲": ".", "⠂": ",", "⠦": "?", "⠖": "!", "⠾": ":", "⠆": ";",
                "⠄": """, "⠤": "-", "⠌": "/", "⠷": "(", "⠾": ")", "⠶": """, "\n": "\n"}
            englishtranslation = "".join(englishdict.get(char, "") for char in text)
            print(englishtranslation)
            translated=translate(englishtranslation,"en")
            speak(englishtranslation)
            """
            NOT ALL LANGUAGES CAN BE SPOKEN BY THE TEXT TO SPEECH ENGINE
            ONLY THOSE LANGUAGES WITH ENGLISH CHARACTERS CAN BE SPOKEN
            """

        def recogniseaudiofile(lang):
            """Recognize speech"""
            filepath=audiodirectory.get()
            try:
                with sr.AudioFile(filepath) as source:
                    speak("Processing uploaded audio file...")
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio)
                    speak(f"Recognized Text: {text}")
                    translated=translate(text,lang)
                    brailleoutput = audiotobraille(translated)
                    print(f"Braille Representation: {brailleoutput}")
            except sr.UnknownValueError:
                speak("Could not understand the audio in the file.")
            except sr.RequestError as e:
                speak(f"Recognition service error:{e}")
                
        def listenforsound(lang):
            global a
            a=1
            # Use the microphone as the audio source
            with sr.Microphone() as source:
                speak("Please say something...")
                # Adjust for ambient noise and record audio
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                speak("Recognizing...")

                try:
                    # Use Google Web Speech API to recognize the audio
                    text1 = recognizer.recognize_google(audio)
                    translated=translate(text1,lang)
                    audiotobraille(translated)
                    # Repeat the recognized text
                    speak(f"You said: "+text1)
                    a=0

                except sr.UnknownValueError:
                    speak("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    speak(f"Could not request results from Google Speech Recognition service; {e}")
            a=0
            threading.Thread(target=listenforcommandaudio, daemon=True).start()

        def aioverview():
            global a
            a=1
            input_braille = brailleinput.get("0.0", "end").strip()
            output_braille = brailleoutput.cget("text").strip()
            brailechars = set("⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵⠼⠲⠂⠦⠖⠾⠆⠄⠤⠌⠷⠶")
            def isbraille(text):
                return any(c in brailechars for c in text)
            explaintext = ""
            englishdict = {
                "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
                        "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
                        "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
                        "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
                        "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽",
                        "z": "⠵", " ": " ", "\n":"\n", "1":"⠼⠁", "2":"⠼⠃",
                        "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛",
                        "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚", ",": "⠂", ";": "⠆",
                        ":": "⠒", ".": "⠲", "?": "⠦", "!": "⠖", """: "⠄", "|":"⠖",
                        """: "⠄⠶", "(": "⠐⠣", ")": "⠐⠜", "/": "⠸⠌", "-": "⠤",
                        "_": "⠐⠠⠤", "<":" ", ">":" ", "{":" ", "}":" ","@":" ",
                        "#":" ", "$":" ", "%":" ", "^":" ", "&":" ", "*":" ", "+":" ",
                        "=":" ", "“":"⠘⠦", "”":"⠘⠴", "‘":"⠄⠦", "’":"⠄⠴", "–":"⠠⠤", "—":"⠐⠠⠤",
                        "©":" ", "°":" ", "÷":" ", "¡":" ", "¿":" ", "®":" ",
                        "~":" ", "™":" ", "«":" ", "»":" ", "€":" ", "¢":" ","\\":" ", "[":" ",
                        "]":" ", "é":" ", "§":" ", "¥":" ", "£":" ", "₨":" ", "₹":" ", "₩":" ",
                        "₺":" ", "₼":" ","₽":" ", "₿":" ", "₼":" "
            }
            def braille_to_english(text):
                i = 0
                englishtext = ""
                while i < len(text):
                    if text[i] == "⠼" and i+1 < len(text):
                        num = text[i:i+2]
                        englishtext += englishdict.get(num, "")
                        i += 2
                    else:
                        englishtext += englishdict.get(text[i], "")
                        i += 1
                return englishtext

            if input_braille and isbraille(input_braille):
                explaintext = braille_to_english(input_braille)
            elif output_braille and isbraille(output_braille):
                explaintext = braille_to_english(output_braille)
            else:
                explaintext = ""

            if explaintext:
                try:
                    messages = [
                        {'role': 'system', 'content': 'Be concise and precise. Reply in max 6-7 continuous sentences and include only essential details and use only alphabetic characters. Avoid using punctuation marks like commas, periods, or quotation marks.'},
                        {'role': 'user', 'content': explaintext},
                    ]
                    response = chat('deepseek-v3.1:671b-cloud', messages=messages, options={'temperature': 0.2, 'max_tokens': 120})
                    speak(response['message']['content'])
                    
                except Exception as e:
                    tk.messagebox.showerror("AI Overview Error", str(e))
                a=0
                threading.Thread(target=listenforcommandaudio, daemon=True).start()

        audiopageframe =ctk.CTkFrame(pageframe)
        audiopageframe.pack(pady=0,fill="both",expand=True)

        audioframe=ctk.CTkScrollableFrame(audiopageframe,width=width,height=1700,
                                        label_anchor="center",)
        audioframe.pack(pady=0,fill="both",expand=True)

        label1=tk.Label(audioframe,width=1900,height=1000)
        label1.pack()
        vid1=tkvideo(os.path.join(VIDEOS_DIR, "audio_video_1.mp4"), label1, loop=1, size=(1900,1000))
        vid1.play()

        def submit3():
            listenforsound(transkey[lang1.get()])

        audioinput=ctk.CTkButton(audioframe,height=150,text="Click to talk",
                                width=500,font=("Helvetica",18),corner_radius=50,text_color="black",
                                fg_color=menubarcolour,command=submit3)
        audiodirectory=ctk.CTkEntry(audioframe,height=150,
                                width=500,font=("Helvetica",18),corner_radius=50,text_color="black",
                                fg_color=menubarcolour)
        audiodirectory.place(x=100,y=400,anchor="sw")

        audioinput.place(x=100,y=50,anchor="nw")

        def submit2():
            recogniseaudiofile(transkey[lang1.get()])

        submit=ctk.CTkButton(audioframe,text="Submit directory",command=submit2,corner_radius=50,bg_color="transparent",
                            fg_color=menubarcolour,text_color="black")
        submit.place(x=100,y=450,anchor="sw")

        brailleinput=ctk.CTkTextbox(audioframe,height=150,
                                width=500,font=("Helvetica",18),wrap="word",corner_radius=50,text_color="black",
                                fg_color=menubarcolour)

        brailleinput.place(x=100,y=480,anchor="nw")

        lang1 = tk.StringVar()
        lang1.set("Select Language")

        options = ctk.CTkOptionMenu(audioframe, variable=lang1, values=list(transkey.keys()), 
                                    corner_radius=50, fg_color=menubarcolour, text_color="black")
        options.place(x=400,y=680,anchor="sw")

        def submit1():
            brailletoaudio(transkey[lang1.get()])

        submitbraille=ctk.CTkButton(audioframe,text="Submit braille",command=submit1,corner_radius=50,bg_color="transparent",
                            fg_color=menubarcolour,text_color="black")
        submitbraille.place(x=100,y=680,anchor="sw")

        brailleoutput=ctk.CTkLabel(audioframe,text="",width=600,height=500,
                                    corner_radius=50,justify="left",
                                    fg_color=menubarcolour,bg_color="transparent",
                                    text_color="black",font=("Arial",20))
        brailleoutput.place(x=800,y=150,anchor="nw")

        aibutton = ctk.CTkButton(
            audiopageframe,
            text="AI Overview",
            command=aioverview,
            corner_radius=50,
            fg_color=menubarcolour,
            text_color="black",
            font=("Arial", 18)
        )
        aibutton.place(x=1400, y=50, anchor="ne")

        audiopageframe.pack(fill=tk.BOTH, expand=True)
        a=0
        # Start the listening thread
        threading.Thread(target=listenforcommandaudio, daemon=True).start()

def imagepage():
    global menubarcolour
    global t,l,a,i,h
    i=1
    if i==1 and a==0 and l==0 and t==0 and h==0:
        def listenforcommandimage():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                while a==0:
                    speak("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        speak(f"You said: {command}")
                        print(command)
                        processcommandimage(command)  # Process the recognized command
                        i=0
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        def processcommandimage(command):
            global i
            # Here you can define how to handle different commands
            command = command.lower()
            if "what is your name" in command:
                speak("I am Nirvana, your voice assistant.")
            
            elif "go to" in command:
                
                if "text converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    i=0
                    textpage()
                elif "audio converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    i=0
                    audiopage()
                elif "image converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    i=0
                    imagepage()
                elif "home" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    i=0
                    homepage()
                elif "help page" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    i=0
                    helppage()
            elif "theme is" in command:
                changetheme(command)

            elif "exit" in command :
                speak("Goodbye!")
                root.quit()  # Close the Tkinter app

            elif "no sound" in command:
                
                global sound_enabled
                sound_enabled=False
            elif "submit" in command:
                if "text to image" in command:
                    texttoimage()
                elif "image to braille" in command:
                    imagetobraille()
            elif "help" in command or "ai overview" in command or "eye overview" in command or "ai" in command:
                aioverview()
            elif "image input" in command or "image in" in command:
                imageinput.focus_set()
            elif "braille" in command or "other" in command or "brain" in command:
                brailleoutput.focus_set()
            elif "image directory" in command or "image" in command:
                imagedirectory.focus_set()
            else:
                print(command)
                pass
        def texttoimage():
            mapbraille = {}

            def getbraille(text):
                b = ""
                file = open(os.path.join(DATA_DIR, "braille_letters (1)(1).csv"), "r", encoding="utf-8")
                csv_reader = csv.reader(file)

                for i in csv_reader:
                    char = i[1]
                    key = eval(char.strip())

                    mapbraille[i[0]] = key

                for t in text:
                    if t=="\n":
                        b+=t
                    else:
                        b += mapbraille[t]
                return b

            text=imageinput.get("0.0","end").lower()
            text=text.strip()

            sleep(5)

            text=str(text)
            b = getbraille(text)

            wrap_text = tw.fill(b, width = 45)

            img = Image.new(mode="RGB", size=(1500,1500), color=(173,216,230))
            d = ImageDraw.Draw(img)

            font = ImageFont.truetype(os.path.join(FONTS_DIR, "BrailleCc0-DOeDd.ttf"), 100)

            x = 100
            y = 100

            d.multiline_text((x,y),text=b,font=font,spacing=10,fill=("black"),align="left")

            output_dir = os.path.join(RESOURCES_DIR, "output")
            os.makedirs(output_dir, exist_ok=True)  # Create if needed
            img.save(os.path.join(output_dir, "braille_image.png"))
            img1=ctk.CTkImage(dark_image=img,size=(550,450))
            brailleoutput.configure(image=img1,text="")
            img.show()

        def imagetobraille():
            mapbraille = {}

            def getbraille(text):
                b = ""
                file = open(os.path.join(DATA_DIR, "braille_letters (1).csv"), "r", encoding="utf-8")
                csv_reader = csv.reader(file)

                for i in csv_reader:
                    char = i[1]
                    key = eval(char.strip())
                    mapbraille[i[0]] = key

                for t in text:
                    if t == "\n":
                        b+= "\n"
                    else: 
                        b += mapbraille[t]
                return b
            
            file = imagedirectory.get()
            tesseract_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

            pyt.pytesseract.tesseract_cmd = tesseract_path

            img = Image.open(file)
            img.show()

            txt = pyt.image_to_string(img)
            print(txt)
            x=""
            a=0
            for i in range(len(txt)):
                if a<40:
                    x+=(getbraille(txt[i].lower()))
                    a+=1
                else:
                    x+="\n"
                    a=0

            brailleoutput.configure(text=x,image="")

        def aioverview():
            global a
            a=0
            inputtext = imageinput.get("0.0", "end").strip()
            outputtext = brailleoutput.cget("text").strip()

            brailechars = set("⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵⠼⠲⠂⠦⠖⠾⠆⠄⠤⠌⠷⠶")
            def isbraille(text):
                return any(c in brailechars for c in text)
            explaintext = ""
            if outputtext and isbraille(outputtext):
                
                englishdict = {
                    "⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e", "⠋": "f", "⠛": "g",
                    "⠓": "h", "⠊": "i", "⠚": "j", "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n",
                    "⠕": "o", "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s", "⠞": "t", "⠥": "u",
                    "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y", "⠵": "z",
                    "⠼⠁": "1", "⠼⠃": "2", "⠼⠉": "3", "⠼⠙": "4", "⠼⠑": "5", "⠼⠋": "6",
                    "⠼⠛": "7", "⠼⠓": "8", "⠼⠊": "9", "⠼⠚": "0",
                    " ": " ", "⠲": ".", "⠂": ",", "⠦": "?", "⠖": "!", "⠾": ":", "⠆": ";",
                    "⠄": """, "⠤": "-", "⠌": "/", "⠷": "(", "⠾": ")", "⠶": """, "\n": "\n"
                }
                
                i = 0
                englishtext = ""
                while i < len(outputtext):
                    if outputtext[i] == "⠼" and i+1 < len(outputtext):
                        num = outputtext[i:i+2]
                        englishtext += englishdict.get(num, "")
                        i += 2
                    else:
                        englishtext += englishdict.get(outputtext[i], "")
                        i += 1
                explaintext = englishtext
            elif inputtext:
                explaintext = inputtext
            if explaintext:
                try:
                    messages = [
                        {'role': 'system', 'content': 'Be concise and precise. Reply in max 6-7 continuous sentences and include only essential details and use only alphabetic characters. Avoid using punctuation marks like commas, periods, or quotation marks.'},
                        {'role': 'user', 'content': explaintext},
                    ]
                    response = chat('deepseek-v3.1:671b-cloud', messages=messages, options={'temperature': 0.2, 'max_tokens': 120})
                    speak(response['message']['content'])
                    
                except Exception as e:
                    tk.messagebox.showerror("AI Overview Error", str(e))
                a=0

        imagepageframe =ctk.CTkFrame(pageframe)
        imagepageframe.pack(pady=0,fill="both",expand=True)

        imageframe=ctk.CTkScrollableFrame(imagepageframe,width=width,height=1700,
                                        label_anchor="center",)
        imageframe.pack(pady=0,fill="both",expand=True)

        label1=tk.Label(imageframe,width=1900,height=1000)
        label1.pack()
        vid1=tkvideo(os.path.join(VIDEOS_DIR, "image_video.mp4"), label1, loop=1, size=(1900, 1000))
        vid1.play()

        imageinput=ctk.CTkTextbox(imageframe,height=150,
                                width=500,font=("Helvetica",18),wrap="word",corner_radius=50,text_color="black",
                                fg_color=menubarcolour)
        
        imageinput.place(x=100,y=150,anchor="nw")

        submit=ctk.CTkButton(imageframe,text="Submit",command=texttoimage,corner_radius=50,bg_color="transparent",
                            fg_color=menubarcolour,text_color="black")
        submit.place(x=100,y=350,anchor="sw")

        imagedirectory=ctk.CTkEntry(imageframe,height=150,
                                width=500,font=("Helvetica",18),corner_radius=50,text_color="black",
                                fg_color=menubarcolour)
        imagedirectory.place(x=100,y=600,anchor="sw")

        submit=ctk.CTkButton(imageframe,text="Submit directory",command=imagetobraille,corner_radius=50,bg_color="transparent",
                            fg_color=menubarcolour,text_color="black")
        submit.place(x=100,y=650,anchor="sw")

        brailleoutput=ctk.CTkLabel(imageframe,width=600,height=500,justify="left",
                                    corner_radius=50,text="",image="",
                                    fg_color=menubarcolour,bg_color="transparent",
                                    text_color="black",font=("Arial",20))
        brailleoutput.place(x=800,y=150,anchor="nw")

        aibutton = ctk.CTkButton(
            imagepageframe,
            text="AI Overview",
            command=aioverview,
            corner_radius=50,
            fg_color=menubarcolour,
            text_color="black",
            font=("Arial", 18)
        )
        aibutton.place(x=1400, y=50, anchor="ne")

        imagepageframe.pack(fill=tk.BOTH, expand=True)
        i=0
        # Start the listening thread
        threading.Thread(target=listenforcommandimage, daemon=True).start()

def helppage():
    global menubarcolour
    global t,l,a,i,h
    l=1
    if l==1 and a==0 and h==0 and t==0 and i==0:
        def listenforcommandhelp():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                while a==0:
                    speak("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    try:
                        command = recognizer.recognize_google(audio)
                        speak(f"You said: {command}")
                        processcommandhelp(command)  # Process the recognized command
                        l=0
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        def processcommandhelp(command):
            global l
            # Here you can define how to handle different commands
            command = command.lower()
            if "what is your name" in command:
                speak("I am Nirvana, your voice assistant.")
           
            elif "go to" in command:   
                if "text converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    l=0
                    textpage()
                elif "audio converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    l=0
                    audiopage()
                elif "image converter" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    l=0
                    imagepage()
                elif "home" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    l=0
                    homepage()
                elif "help page" in command:
                    for frame in pageframe.winfo_children():
                        frame.destroy()
                    l=0
                    helppage()
            elif "theme is" in command:
                changetheme(command)

            elif "exit" in command :
                speak("Goodbye!")
                root.quit()  # Close the Tkinter app

            elif "no sound" in command:
                
                global sound_enabled
                sound_enabled=False
            elif "start" in command:
                start()
            elif "stop" in command:
                Stop()
            else:
                print(command)
                pass

        global menubarcolour
        def start():
            global running,webcam_ip
            running=True
            user_ip = ctk.CTkInputDialog(text="Enter your IP Webcam IP and port (e.g., 192.0.0.4:8080):", title="Webcam IP").get_input()
            if user_ip and ":" in user_ip:  # Basic validation
                webcam_ip = user_ip
            else:
                speak("Using default IP. Please enter a valid IP:port.")
            livetranslate()

        def livetranslate():
            global running
            if running is True:
                pyt.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

                def convert(text):
                    mapping = {
                        "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
                        "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
                        "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
                        "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
                        "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽",
                        "z": "⠵", " ": " ", "\n":"\n", "1":"⠼⠁", "2":"⠼⠃",
                        "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛",
                        "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚", ",": "⠂", ";": "⠆",
                        ":": "⠒", ".": "⠲", "?": "⠦", "!": "⠖", """: "⠄", "|":"⠖",
                        """: "⠄⠶", "(": "⠐⠣", ")": "⠐⠜", "/": "⠸⠌", "-": "⠤",
                        "_": "⠐⠠⠤", "<":" ", ">":" ", "{":" ", "}":" ","@":" ",
                        "#":" ", "$":" ", "%":" ", "^":" ", "&":" ", "*":" ", "+":" ",
                        "=":" ", "“":"⠘⠦", "”":"⠘⠴", "‘":"⠄⠦", "’":"⠄⠴", "–":"⠠⠤", "—":"⠐⠠⠤",
                        "©":" ", "°":" ", "÷":" ", "¡":" ", "¿":" ", "®":" ",
                        "~":" ", "™":" ", "«":" ", "»":" ", "€":" ", "¢":" ","\\":" ", "[":" ",
                        "]":" ", "é":" ", "§":" ", "¥":" ", "£":" ", "₨":" ", "₹":" ", "₩":" ",
                        "₺":" ", "₼":" ","₽":" ", "₿":" ", "₼":" ",'"': " "
                    }
                    x=""
                    a=0
                    for i in range(len(text)):
                        if a<800:
                            x+=(mapping[text[i].lower()])
                            a+=1
                        else:
                            x+="\n"
                            a=0
                    return x

                try:

                    url = f"http://{webcam_ip}/shot.jpg"  # Use the customizable IP
                    imgresponse = requests.get(url, timeout=5)
                    imgresponse = requests.get(url) #stores binary data of image
                    imgresponse.raise_for_status()  # Raise an error for bad responses
                    imagearray = np.array(bytearray(imgresponse.content), dtype=np.uint8) #converts it into a numpy array

                    img = cv2.imdecode(imagearray, cv2.IMREAD_COLOR) #decodes the array into a cv2 image
                    img = imutils.resize(img, width=750) #resizes the window, while maintaining resolutiion
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converts b&w img to rgb

                    photo = ImageTk.PhotoImage(image=Image.fromarray(img))
                    livefeed.configure(image=photo)
                    livefeed.image = photo  # Keep a reference to avoid garbage collection

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching image: {e}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                textfeed = pyt.image_to_string(img)
                textoutput.configure(text=textfeed)

                output = convert(textfeed)

                brailleoutput.configure(text=output)
                helpframe.after(250,livetranslate)

                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
            
            else:
                livefeed.configure(image="")
                textoutput.configure(text="")
                brailleoutput.configure(text="")
                return

        def Stop():
            global running
            running=False
            livefeed.configure(image="")
            textoutput.configure(text="")
            brailleoutput.configure(text="")

        helppageframe=tk.Frame(pageframe)
        helpframe=ctk.CTkScrollableFrame(helppageframe,width=width,height=1700,
                                        label_anchor="center",)
        
        helpframe.pack(pady=0,fill="both",expand=True)

        Bg=tk.PhotoImage(file=os.path.join(IMAGES_DIR, "help_img(3).png"))

        background1 = ctk.CTkLabel(helpframe, text="", image=Bg)
        background1.configure(width=1800,height=1500)
        background1.pack(pady=0)

        livefeed=ctk.CTkLabel(helpframe,width=600,height=350,justify="left",
                                    corner_radius=50,text="",image="",
                                    fg_color=menubarcolour,bg_color="transparent",
                                    text_color="black",font=("Arial",20))
        livefeed.place(x=50,y=50,anchor="nw")

        textoutput=ctk.CTkLabel(helpframe,width=600,height=650,justify="left",
                                    corner_radius=50,text="",image="",
                                    fg_color=menubarcolour,bg_color="transparent",
                                    text_color="black",font=("Arial",20))
        textoutput.place(x=800,y=50,anchor="nw")

        Start=ctk.CTkButton(helpframe,text="""Start recording""",command=start,corner_radius=50,bg_color="transparent",
        fg_color=menubarcolour,text_color="black",font=("Arial",20))

        Start.configure(height=50,width=100)
        Start.place(x=100,y=600,anchor="sw")

        stop=ctk.CTkButton(helpframe,text="""Stop recording""",command=Stop,corner_radius=50,bg_color="transparent",
        fg_color=menubarcolour,text_color="black",font=("Arial",20))

        stop.configure(height=50,width=100)
        stop.place(x=450,y=600,anchor="sw")

        brailleoutput=ctk.CTkLabel(helpframe,width=1350,height=700,justify="left",
                                    corner_radius=50,text="",image="",
                                    fg_color=menubarcolour,bg_color="transparent",
                                    text_color="black",font=("Arial",20))
        brailleoutput.place(x=50,y=750,anchor="nw")

        helppageframe.pack(fill=tk.BOTH, expand=True)
        l=0
        # Start the listening thread
        threading.Thread(target=listenforcommandhelp, daemon=True).start()

#The start of the actual UI code
pageframe=tk.Frame(root)

pageframe.place(relwidth=1.0, relheight=1.0, x=55)

homepage()

menubarframe=tk.Frame(root, bg=menubarcolour)

def theme(selected):

    global menubarcolour
    menubarcolour = selected
    menubarframe.config(bg=menubarcolour)

    homebutton.config(bg=menubarcolour, activebackground=menubarcolour)
    audiobutton.config(bg=menubarcolour, activebackground=menubarcolour)
    textbutton.config(bg=menubarcolour, activebackground=menubarcolour)
    imagebutton.config(bg=menubarcolour, activebackground=menubarcolour)
    servicesbutton.config(bg=menubarcolour, activebackground=menubarcolour)
    togglemenubutton.config(bg=menubarcolour, activebackground=menubarcolour)

    homebuttonindicator.config(bg=menubarcolour)
    audiobuttonindicator.config(bg=menubarcolour)
    textbuttonindicator.config(bg=menubarcolour)
    imagebuttonindicator.config(bg=menubarcolour)
    servicesbuttonindicator.config(bg=menubarcolour)

    homepagelabel.config(bg=menubarcolour)
    audiopagelabel.config(bg=menubarcolour)
    textpagelabel.config(bg=menubarcolour)
    imagepagelabel.config(bg=menubarcolour)
    servicespagelabel.config(bg=menubarcolour)

    

themes = {
    "default blue": "#1fafc6",
    "red": "#ff5733",
    "green": "#33ff57",
    "blue": "#3357ff",
    "khaki": "#f0e68c",
    "hot pink": "#ff69b4",
    "orange": "#ffa500",
    "purple": "#800080",
    "cyan": "#00ffff",
    "gray": "#808080",
    "pastel pink": "#ffd1dc",
    "pastel blue": "#aec6cf",
    "pastel green": "#77dd77",
    "pastel yellow": "#fdfd96",
    "pastel purple": "#cdb5cd",
    "black": "#000000",
    "white": "#ffffff",
    "pink": "#ffb6c1",
    "gold": "#ffd700",
    "silver": "#c0c0c0"
}

themev = tk.StringVar(value="Select Theme")

themeoption = ctk.CTkOptionMenu(
    menubarframe,
    variable=themev,
    values=list(themes.keys()),
    command=lambda selected: theme(themes[selected]),
    corner_radius=50,
    fg_color="black",
    text_color="white",
    dropdown_fg_color="black",
    dropdown_text_color="white"
)
themeoption.configure(width=90, height=30)
themeoption.place(x=4, y=730)

togglemenubutton=tk.Button(menubarframe, image=toggleicon, bg=menubarcolour,
                          bd=0, activebackground=menubarcolour,
                          command=extend_menu_bar)
togglemenubutton.place(x=8,y=10)

homebutton=tk.Button(menubarframe, image=homeicon,bg=menubarcolour,
                   bd=0, activebackground=menubarcolour,
                   command=lambda: switchindication(indicatorlabel=homebuttonindicator,
                   page=homepage))
homebutton.place(x=12, y=130, width=30,height=40)

homebuttonindicator=tk.Label(menubarframe, bg="white")
homebuttonindicator.place(x=2,y=130,height=40,width=3)

homepagelabel=tk.Label(menubarframe, text="Home", bg =menubarcolour,fg="black",
                    font=("Bold",15),anchor=tk.W)
homepagelabel.place(x=75,y=130,width=100,height=40)
homepagelabel.bind("<Button-1>",lambda e: switchindication(indicatorlabel=homebuttonindicator,page=homepage))

audiobutton=tk.Button(menubarframe, image=audioicon,bg=menubarcolour,
                   bd=0, activebackground=menubarcolour,
                   command=lambda: switchindication(indicatorlabel=audiobuttonindicator,
                   page=audiopage))
audiobutton.place(x=7, y=250, width=40,height=40)

audiopagelabel=tk.Label(menubarframe, text="Audio", bg =menubarcolour,fg="black",
                    font=("Bold",15),anchor=tk.W)
audiopagelabel.place(x=75,y=250,width=100,height=40)
audiopagelabel.bind("<Button-1>",lambda e: switchindication(indicatorlabel=audiobuttonindicator,page=audiopage))

audiobuttonindicator=tk.Label(menubarframe, bg=menubarcolour)
audiobuttonindicator.place(x=2,y=250,height=40,width=3)

textbutton=tk.Button(menubarframe, image=texticon,bg=menubarcolour,
                   bd=0, activebackground=menubarcolour,
                   command=lambda: switchindication(indicatorlabel=textbuttonindicator,
                   page=textpage))
textbutton.place(x=7, y=370, width=40,height=40)

textpagelabel=tk.Label(menubarframe, text="Text", bg =menubarcolour,fg="black",
                    font=("Bold",15),anchor=tk.W)
textpagelabel.place(x=75,y=370,width=100,height=40)
textpagelabel.bind("<Button-1>",lambda e: switchindication(indicatorlabel=textbuttonindicator,page=textpage))

textbuttonindicator=tk.Label(menubarframe, bg=menubarcolour)
textbuttonindicator.place(x=2,y=370,height=40,width=3)

imagebutton=tk.Button(menubarframe, image=imageicon,bg=menubarcolour,
                   bd=0, activebackground=menubarcolour,
                   command=lambda: switchindication(indicatorlabel=imagebuttonindicator,
                   page=imagepage))
imagebutton.place(x=7, y=490, width=40,height=40)

imagepagelabel=tk.Label(menubarframe, text="Image", bg =menubarcolour,fg="black",
                    font=("Bold",15),anchor=tk.W)
imagepagelabel.place(x=75,y=490,width=100,height=40)
imagepagelabel.bind("<Button-1>",lambda e: switchindication(indicatorlabel=imagebuttonindicator,page=imagepage))

imagebuttonindicator=tk.Label(menubarframe, bg=menubarcolour)
imagebuttonindicator.place(x=2,y=490,height=40,width=3)

servicesbutton=tk.Button(menubarframe, image=servicesicon,bg=menubarcolour,
                   bd=0, activebackground=menubarcolour,
                   command=lambda: switchindication(indicatorlabel=servicesbuttonindicator,
                   page=helppage))
servicesbutton.place(x=7, y=610, width=40,height=40)

servicespagelabel=tk.Label(menubarframe, text="Real-Time", bg =menubarcolour,fg="black",
                    font=("Bold",15),anchor=tk.W)
servicespagelabel.place(x=75,y=610,width=100,height=40)
servicespagelabel.bind("<Button-1>",lambda e: switchindication(indicatorlabel=servicesbuttonindicator,page=helppage))
servicesbuttonindicator=tk.Label(menubarframe, bg=menubarcolour)
servicesbuttonindicator.place(x=2,y=610,height=40,width=3)

menubarframe.pack(side=tk.LEFT, fill=tk.Y)
menubarframe.pack_propagate(flag=False)
menubarframe.configure(width=55)

root.mainloop()  
