import pyaudio
import wave
from tqdm import tqdm
import time
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


def record(filename, record_seconds):
    RECORD_SECONDS = record_seconds
    WAVE_OUTPUT_FILENAME = filename

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in tqdm(range(0, int(RATE / CHUNK * RECORD_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)

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


def play(filename):

    wf = wave.open(filename, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return data, pyaudio.paContinue

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()


def simple():
    import simpleaudio as sa
    from pydub import AudioSegment
    from pydub import playback
    mp3 = AudioSegment.from_file("09.mp3", format="mp3")
    print(mp3.duration_seconds)
    playback.play(mp3)