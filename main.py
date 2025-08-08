import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import os
import uuid
import sys
import time


def listen_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Please speak something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("🔍 Processing voice...")
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏰ Timeout! No speech detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand your speech.")
            return None
        except sr.RequestError:
            print("🚫 Speech Recognition service error.")
            sys.exit(1)


def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        print(f"🌐 Translated ({target_language}): {translated}")
        return translated
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return None


def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"🔇 TTS failed: {e}")
        print("📢 Output text instead:")
        print(f"> {text}")


def banner():
    print("=" * 60)
    print("🧠  Multilingual Voice Translator | Deep Translator + gTTS")
    print("=" * 60)
    print("🌍 Supported Language Codes:")
    print("   hi=Hindi | kn=Kannada | ta=Tamil | te=Telugu | mr=Marathi")
    print("   fr=French | es=Spanish | en=English | ml=Malayalam | bn=Bengali")
    print("-" * 60)


def main():
    banner()
    target_lang = input("📝 Enter target language code: ").strip().lower()

    print("\n✅ Ready! Press Enter to start translating your voice...\n")

    while True:
        input("🎤 Press ENTER and start speaking after the prompt...")
        voice_text = listen_voice_input()

        if voice_text:
            translated = translate_text(voice_text, target_lang)
            if translated:
                speak_text(translated, lang_code=target_lang)

        again = input("\n🔁 Do you want to translate another sentence? (y/n): ").strip().lower()
        if again != 'y':
            print("\n👋 Thank you for using the Multilingual Voice Translator!")
            time.sleep(1)
            break


if __name__ == "__main__":
    main()

