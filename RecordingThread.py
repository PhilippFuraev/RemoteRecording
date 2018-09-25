from tkinter import *
import pyaudio
import wave
import threading
from pydub import AudioSegment
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 128000
WAVE_OUTPUT_FILENAME = "output.wav"
FFMPEG_DESTINATION = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
class RecordingThread(threading.Thread):

    def __init__(self):
        super(RecordingThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if self.stopped():
                print("* done recording")

                stream.stop_stream()
                stream.close()
                p.terminate()

                wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                break

def wavToFlac():
    AudioSegment.converter = FFMPEG_DESTINATION
    song = AudioSegment.from_wav("output.wav")
    song.export("dialog.flac", format="flac", bitrate="256k")