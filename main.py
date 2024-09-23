from openai import OpenAI
import os
import wave
import pyaudio
from dotenv import load_dotenv
import markdown2 as m2
from messages import homePath, audioFilePath
import os
from groq import Groq

clientSTT = Groq(api_key=f'{os.getenv("API_KEY_STT")}')   
load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return m2.markdown(response.choices[0].message.content)
def recorder(filename, duration=5, sample_rate=44100, chunk=1024, channels=1):
    audio_format = pyaudio.paInt16
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    frames = []
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
def audio_to_text(filename="audio.webm"):
    AUDIO_FILE = homePath+audioFilePath+"/"+filename
    try:
        with open(AUDIO_FILE, "rb") as file:
            transcription = clientSTT.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )
        return transcription.text
    except:
        return False
    


'''text = input("Do you want to type or speak? T/S")
recited = input("Do you want to recite the response? Y/N")
if text.lower() == "t":
    prompt = input("Enter your prompt: ")
    #response = get_response(prompt)
elif text.lower() == "s":
    recorder("audio.wav", duration=int(input("Enter the duration of the recording in seconds: ")))
    #response = get_response(audio_to_text("audio.wav"))
    response = audio_to_text("audio.wav")
else :
    print("Invalid input")

if recited.lower() == "y":
    recite(response)
elif recited.lower() == "n":
    print("response")'''