import sys
from queue import Queue
from ctypes import POINTER, c_ubyte, c_void_p, c_ulong, cast
from collections import deque
import time

# The majority of this code is from
# https://menno.io/posts/pulseaudio_monitoring/

from pulseaudio.lib_pulseaudio import *

SINK_NAME = bytes(
    'alsa_output.pci-0000_03_00.6.analog-stereo', encoding='utf-8')
#SINK_NAME = bytes(
#    'alsa_output.pci-0000_03_00.1.hdmi-stereo', encoding='utf-8')
METER_RATE = 344
METER_RATE = 172 # two
METER_RATE = int(172/4) # test
MAX_SAMPLE_VALUE = 127
DISPLAY_SCALE = 0
MAX_SPACES = MAX_SAMPLE_VALUE >> DISPLAY_SCALE


class PeakMonitor(object):

    def __init__(self, sink_name, rate):
        self.sink_name = sink_name
        self.rate = rate

        # Wrap callback methods in appropriate ctypefunc instances so
        # that the Pulseaudio C API can call them
        self._context_notify_cb = pa_context_notify_cb_t(
            self.context_notify_cb)
        self._sink_info_cb = pa_sink_info_cb_t(self.sink_info_cb)
        self._stream_read_cb = pa_stream_request_cb_t(self.stream_read_cb)

        # stream_read_cb() puts peak samples into this Queue instance
        self._samples = Queue()

        # Create the mainloop thread and set our context_notify_cb
        # method to be called when there's updates relating to the
        # connection to Pulseaudio
        _mainloop = pa_threaded_mainloop_new()
        _mainloop_api = pa_threaded_mainloop_get_api(_mainloop)
        context = pa_context_new(
            _mainloop_api, bytes("peak_demo", encoding='utf-8'))
        pa_context_set_state_callback(context, self._context_notify_cb, None)
        pa_context_connect(context, None, 0, None)
        pa_threaded_mainloop_start(_mainloop)

    def __iter__(self):
        while True:
            yield self._samples.get()

    def context_notify_cb(self, context, _):
        state = pa_context_get_state(context)

        if state == PA_CONTEXT_READY:
            print("Pulseaudio connection ready...")
            # Connected to Pulseaudio. Now request that sink_info_cb
            # be called with information about the available sinks.
            o = pa_context_get_sink_info_list(
                context, self._sink_info_cb, None)
            pa_operation_unref(o)

        elif state == PA_CONTEXT_FAILED:
            print("Connection failed")

        elif state == PA_CONTEXT_TERMINATED:
            print("Connection terminated")

    def sink_info_cb(self, context, sink_info_p, _, __):
        if not sink_info_p:
            return

        sink_info = sink_info_p.contents
        print('-' * 60)
        print('index:', sink_info.index)
        print('name:', sink_info.name)
        print('description:', sink_info.description)

        if sink_info.name == self.sink_name:
            # Found the sink we want to monitor for peak levels.
            # Tell PA to call stream_read_cb with peak samples.
            print('setting up peak recording using',
                  sink_info.monitor_source_name)
            samplespec = pa_sample_spec()
            samplespec.channels = 1
            samplespec.format = PA_SAMPLE_U8
            samplespec.rate = self.rate

            pa_stream = pa_stream_new(context, bytes(
                "pd demo", encoding='utf-8'), samplespec, None)
            pa_stream_set_read_callback(pa_stream,
                                        self._stream_read_cb,
                                        sink_info.index)
            pa_stream_connect_record(pa_stream,
                                     sink_info.monitor_source_name,
                                     None,
                                     PA_STREAM_PEAK_DETECT)

    def stream_read_cb(self, stream, length, index_incr):
        data = c_void_p()
        pa_stream_peek(stream, data, c_ulong(length))
        data = cast(data, POINTER(c_ubyte))
        for i in range(length):
            # When PA_SAMPLE_U8 is used, samples values range from 128
            # to 255 because the underlying audio data is signed but
            # it doesn't make sense to return signed peaks.
            self._samples.put(data[i])
        pa_stream_drop(stream)


def dry_run():
    monitor = PeakMonitor(SINK_NAME, METER_RATE)
    for sample in monitor:
        sample = sample >> DISPLAY_SCALE
        bar = '>' * sample
        spaces = ' ' * (MAX_SPACES - sample)
        print('\r%s ' % sample)
        sys.stdout.flush()


def main(dm, history_length=1000, send_timeout=8):
    monitor = PeakMonitor(SINK_NAME, METER_RATE)
    previous_peaks = deque(maxlen=history_length)
    for sample in monitor:
        sample = sample - 128
        #sample *= 2
        #assert sample <= 256

        previous_peaks.appendleft(sample)
        brightness_min = 0
        brightness_max = 255
        brightness = 0
        if (max(previous_peaks)-min(previous_peaks)) != 0:
            brightness = (sample-min(previous_peaks))/(max(previous_peaks)-min(previous_peaks))*(brightness_max-brightness_min)+brightness_min
        #brightness = sum(previous_peaks) / len(previous_peaks)
        #print(brightness)
        #print(max(previous_peaks))
        send_start_time = time.time()*1000 # ms
        for station in dm.getDevices():
            dm.sendColorSpecific(
                {
                    'r': (0),
                    'g': (0),
                    'b': (int(brightness)),
                },
                station['id'])
            if ((time.time()*1000) - send_start_time) > send_timeout:
                #print("send timeout!")
                while not monitor._samples.empty():
                    monitor._samples.get()
                break


if __name__ == '__main__':
    dry_run()
