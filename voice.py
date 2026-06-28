try:
    import speech_recognition as sr
    import pyttsx3
    import threading

    VOICE_AVAILABLE = True

    try:
        engine = pyttsx3.init()
    except Exception:
        engine = None
        VOICE_AVAILABLE = False

    engine_lock = threading.Lock()

except Exception:
    VOICE_AVAILABLE = False
    engine = None


# ===============================
# 🔊 VOICE CONFIGURATION
# ===============================
def set_voice(style="default", rate=180, volume=1.0):

    if not VOICE_AVAILABLE or engine is None:
        return

    voices = engine.getProperty("voices")

    if style == "female" and len(voices) > 1:
        engine.setProperty("voice", voices[1].id)
    else:
        engine.setProperty("voice", voices[0].id)

    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)


# ===============================
# 🔊 SPEAK
# ===============================
def speak(text):

    if not VOICE_AVAILABLE or engine is None:
        return

    if not text:
        return

    def run():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()

    threading.Thread(target=run).start()


# ===============================
# 🛑 STOP SPEAKING
# ===============================
def stop_speaking():

    if not VOICE_AVAILABLE or engine is None:
        return

    with engine_lock:
        engine.stop()


# ===============================
# 🎤 LISTEN
# ===============================
def listen(timeout=5, phrase_time_limit=10):

    if not VOICE_AVAILABLE:
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        return recognizer.recognize_google(audio)

    except Exception:
        return ""