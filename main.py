import speech_recognition as sr
import speak
import chatbot as chat

r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        try:
            #print("Werner hört zu!")
            #audio = r.listen(source)
            #input = r.recognize_google(audio, language="de-DE")

            response = chat.chat(input(">"))
            print(response)
            #speak.speakText(response)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))