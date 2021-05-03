def speech():
    import speech_recognition as sr
    r = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")


        # recognize speech using google

        try:
            text =  r.recognize_google(audio)


        except Exception as e:
            print("Error :  " + str(e))
    return text
