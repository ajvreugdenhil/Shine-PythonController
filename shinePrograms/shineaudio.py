import math
import shutil
import numpy as np
import sounddevice as sd


audio_device = 2
block_duration = 1
gain = 3200
low = 100
high = 2000
columns = 80
channel_amount = 1
test_freq = 4

device_dict = sd.query_devices()
print(device_dict)
print("#########")
print(sd.query_devices(audio_device, 'input'))
print("#########")
samplerate = sd.query_devices(audio_device, 'input')['default_samplerate']
delta_f = (high - low) / (columns - 1)
fftsize = math.ceil(samplerate / delta_f)
low_bin = math.floor(low / delta_f)
blocksize = samplerate * block_duration / 1000


def audio_callback(indata, frames, time, status):
    magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
    magnitude *= gain / fftsize
    volume = int(int(magnitude[16]) * int(magnitude[16]) / 2)
    # print(volume)
    if volume > 255:
        volume = 255
    dm.sendColorSpecific(
        {"r": 0, "g": volume, "b": volume}, '30847e')


def main():
    with sd.InputStream(device=audio_device, channels=1, callback=audio_callback,
                        blocksize=int(blocksize),
                        samplerate=samplerate):
        while True:
            pass
