import json
import pyaudio
import threading
from queue import Queue


def get_streamer(callback, chunk):
    """ initialize a new streamer """

    def inner_callback(in_data, frame_count, time_info, status):
        callback(in_data)
        return (None, pyaudio.paContinue)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2,
                        rate=44100, input=True, frames_per_buffer=chunk,
                        stream_callback=inner_callback)
    return stream


def get_player():
    """ initialize a new player """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2,
                        rate=44100, output=True)
    return stream


class CallAPI:

    def __init__(self, api, username, sock):
        self.api = api
        self.username = username
        self.sock = sock
        self.on_talk = False

    def idle(self):
        while True:
            self.api.update_my_address(self.sock)
            self.on_talk = False
            self.call(input("call: ").lower())

    def call(self, username):
        print("calling " + username)

        addr = None
        try:
            addr = self.api.get_address(username)
        except:
            pass

        if not addr:
            print("{} is not available".format(username))
            self.idle()
            return

        host, port = addr.split(":")
        print(addr)
        self.process_call((host, int(port)))

    def process_call(self, recp):
        self.on_talk = True
        player = get_player()
        queue = Queue()

        def stream_handle(data):
            self.sock.sendto(data, recp)

        def process():
            while self.on_talk:
                data, addr = self.sock.recvfrom(1024)
                queue.put(data)

        def speak():
            while self.on_talk:
                if not queue.empty():
                    player.write(queue.get())

        thread = threading.Thread(target=process)
        thread1 = threading.Thread(target=speak)
        streamer = get_streamer(stream_handle, 1024)
        streamer.start_stream()
        thread.start()
        thread1.start()

        while True:
            if input("End (Y) ") == "Y":
                streamer.stop_stream()
                return

    @staticmethod
    def bin2json(bin_json):
        return json.loads(bin_json.decode())

    @staticmethod
    def json2bin(js):
        return json.dumps(js).encode()
