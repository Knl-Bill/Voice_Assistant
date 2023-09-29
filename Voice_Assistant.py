import speech_recognition as sr
from gtts import gTTS
import pygame
import openai
import json
import os
OPENAI_API_KEY = ""
with open('config.json','r') as f:
    f_data = json.load(f)
    OPENAI_API_KEY = f_data["OPENAI_API_KEY"]
while(1):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source,timeout=5)
            text = recognizer.recognize_google(audio)
            print(text)
        except sr.WaitTimeoutError:
            print("No audio detected")
            continue
    check_termination = text.replace(' ','')
    check_termination = check_termination.lower()
    if(check_termination == "shutdown"):
        break
    openai.api_key = OPENAI_API_KEY
    context = ""
    with open('Bot1.txt','r') as cnt:
        context = cnt.readlines()
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role":"system", "content":f"{context} and if you are asked any question about yourself, strictly stick to the context provided to you"},
            {"role":"user", "content": text}
        ]
    )
    text = completion['choices'][0]['message']['content']
    tts = gTTS(text,lang='en',slow=False)
    path = os.getcwd()
    path += "/tts.mp3"
    tts.save(path)
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    audio_duration = pygame.mixer.Sound(path).get_length()
    pygame.time.delay(int(audio_duration * 1000))
    pygame.mixer.quit()