#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os,io
import speech_recognition as sr
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:/Users/Samden/Desktop/Data Science/Hackathon/PnG/google-api.json'


# In[20]:


local_file_path='Audio Files/recorded.wav'


# In[59]:


from google.cloud import speech_v1
import io


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using an enhanced model

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/hello.wav'

    # The enhanced model to use, e.g. phone_call
    model = "phone_call"

    # Use an enhanced model for speech recognition (when set to true).
    # Project must be eligible for requesting enhanced models.
    # Enhanced speech models require that you opt-in to data logging.
    use_enhanced = True

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "model": model,
        "use_enhanced": use_enhanced,
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        for i in len(alternative.transcript):
        print(u"{}".format(alternative.transcript))


# In[58]:


import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    print("Please say something")

    audio = r.listen(source)

    print("Recognizing Now .... ")

    with open("Audio Files/recorded.wav", "wb") as f:
        f.write(audio.get_wav_data())


# In[60]:


print(sample_recognize(local_file_path))

