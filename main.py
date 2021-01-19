import argparse
from shineController import controller
import time
import datetime
import signal
import sys
import json
import time
from fftsource.stream_analyzer import Stream_Analyzer

c = None

colorChannels = ["r", "g", "b"]

def sigint_handler(sig, frame):
    global c
    if c is not None:
        c.setColorGlobal({"r": 0, "g": 0, "b": 0})
        del c
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=None, dest='device',
                        help='pyaudio (portaudio) device index')
    parser.add_argument('--n_frequency_bins', type=int, default=400, dest='frequency_bins',
                        help='The FFT features are grouped in bins')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
                        help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args()

def main():
    args = parse_args()

    ear = Stream_Analyzer(
                    device = args.device,        # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = None,               # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 30,    # Window size used for the FFT transform. was 60
                    updates_per_second  = 1000,  # How often to read the audio stream for new data
                    smoothing_length_ms = 50,    # Apply some temporal smoothing to reduce noisy features. was 50
                    n_frequency_bins = args.frequency_bins, # The FFT features are grouped in bins
                    verbose   = args.verbose,    # Print running statistics (latency, fps, ...)
                    )

    settings = {}
    try:
        programfile = open("./settings.json", "r")
        settings = json.load(programfile)
    except:
        print("Problem with reading the file")
        sys.exit(1)
    try:
        broacastip = settings["broadcastip"]
        port = settings["port"]
        stationIDs = settings["stations"]
    except:
        print("Settings file invalid!")
        sys.exit(1)

    # Initial setup
    foundStationIds = []
    for station in controller.getStations(broacastip, port):
        foundStationIds.append(station["id"])
        if station["id"] not in stationIDs:
            print("Rogue station will not be used: " + station["id"])

    global c
    #c = controller.controller(broacastip, port, stationIDs)
    c = controller.controller(broacastip, port)
    c.setColorGlobal({"r": 0, "g": 0, "b": 0})

    fps = 10  #How often to update the FFT features + display
    last_update = time.time()
    while True:
        if (time.time() - last_update) > (1./fps):
            last_update = time.time()
            raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()
            volume = int(binned_fft[4])
            print(raw_fft[4], binned_fft[4])
            if volume > 255:
                volume = 255
            c.setColorGlobal({"r": volume, "g": volume, "b": volume})
        elif args.sleep_between_frames:
            time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)

if __name__ == '__main__':
    main()