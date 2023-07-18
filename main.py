import speech_recognition as sr
import speak
import chatbot as chat

dochat = True #False to use voice recognition, True to use console to chat

r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        try:
            if dochat:
                prompt = input(">")
            else:
                print("Werner hört zu!")
                prompt = r.recognize_google(r.listen(source), language="de-DE")

            response = chat.chat(prompt)
            print(response)
            speak.speakText(response)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))