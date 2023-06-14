import streamlit as st
import speech_recognition as sr
import time
import os
import pywhatkit as kit
from streamlit_option_menu import option_menu
from selenium import webdriver
from newspaper import Article
from gtts import gTTS


paths = {
    'discord': "C:\\Users\\Acer\\AppData\\Local\\Discord\\app-1.0.9013\\Discord.exe",
}


def open_youtube():
    driver = webdriver.Chrome()  # Change to the appropriate driver for your browser
    driver.get("https://www.youtube.com")
    time.sleep(20)
    driver.quit()


def search_on_wikipedia(query):
    driver = webdriver.Chrome()  # Change to the appropriate driver for your browser
    driver.get("https://en.wikipedia.org/wiki/" + query)
    time.sleep(20)
    driver.quit()


def open_dc():
    os.startfile(paths['discord'])


def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+62{number}", message)


def tts_article(url):
    toi_article = Article(url, language="en")
    toi_article.download()
    toi_article.parse()
    toi_article.nlp()

    st.title("Article's:")
    berita = toi_article.text
    return berita


def mic_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)

    try:
        st.text("Recognizing...")
        text = r.recognize_google(audio, language="id-ID")
        st.text("You Said: {}".format(text))
        return text.lower()
    except sr.UnknownValueError:
        st.warning("Maaf, suara tidak dikenali.")
    except sr.RequestError:
        st.error("Maaf, terjadi kesalahan pada layanan pengenalan suara.")

    return ""


def text_to_speech_id(text):
    bahasa = "id"
    file = gTTS(text=text, lang=bahasa)
    file.save("hallo.mp3")
    audio_file = open("hallo.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")


def text_to_speech_eng(text):
    bahasa = "en"
    file = gTTS(text=text, lang=bahasa)
    file.save("hallo.mp3")
    audio_file = open("hallo.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")


def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Projek PTU B-3",
            options=["Home", "Speech Recognition", "Text To Speech"],
            icons=["house", "mic-fill", "card-text"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Home":
        st.title(selected)
        st.subheader("Kelompok 3")
        st.write("15-2020-012 Mahzuz Hazman")
        st.write("15-2020-013 Omega Putra Adam Josa")
        st.write("15-2020-012 Erlangga")
        st.write("15-2020-012 Rafi Haidar")

    # Bagian Speech Recognition
    if selected == "Speech Recognition":
        st.title(selected)

        if st.button("Start Recording"):
            text = mic_input()
            if text:
                if "youtube" in text:
                    open_youtube()
                elif "discord" in text:
                    open_dc()
                elif "wikipedia" in text:
                    query = text.replace("wikipedia", "").strip()
                    search_on_wikipedia(query)
        st.title("Send Whatsapp Message")
        number = st.text_input("Enter Number:")
        if st.button("Record"):
            message = mic_input()
            send_whatsapp_message(number, message)

    # Bagian Text-to-Speech
    if selected == "Text To Speech":
        st.title(selected)
        text = st.text_input("Enter news link")

        if st.button("Bahasa Indonesia"):
            if text:
                berita = tts_article(text)
                st.write(berita)
                text_to_speech_id(berita)
            else:
                st.warning("Please enter some text.")

        if st.button("Bahasa Inggris"):
            if text:
                berita = tts_article(text)
                st.write(berita)
                text_to_speech_eng(berita)
            else:
                st.warning("Please enter some text.")


if __name__ == "__main__":
    main()
