import sys
sys.path.append("..")
from audio.audio import record

record("voice.wav", 5)
