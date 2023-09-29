from abc import ABC, abstractmethod
from sys import platform
import socket
import threading
from multiprocessing.pool import ThreadPool


class ServerBase(ABC):
    def __init__(self):
        self._is_running = threading.Event()
        self._socket = None
        self._listen_thread = None
        self._connections_thread_pool = None

    def start(self, address='127.0.0.1', port=22, timeout=1):
        if not self._is_running.is_set():
            self._is_running.set()

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

            if platform == "linux" or platform == "linux2":
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)

            self._socket.settimeout(timeout)
            self._socket.bind((address, port))

            self._listen_thread = threading.Thread(target=self._listen)
            self._listen_thread.start()

            self._connections_thread_pool = ThreadPool()

    def stop(self):
        if self._is_running.is_set():
            self._is_running.clear()
            self._listen_thread.join()
            self._socket.close()

    def _listen(self):
        while self._is_running.is_set():
            try:
                self._socket.listen()
                client, addr = self._socket.accept()
                # use apply() to debug errors
                self._connections_thread_pool.apply_async(self.connection_function, args=(client, addr))
            except socket.timeout:
                pass

    @abstractmethod
    def connection_function(self, client, addr):
        """
        This will let us create derived classes of ServerBase that specify their own way of dealing with the connection
        that is being made. For example, later on in our SSH server class, we will connect the SSH Transport objects to
        the connected client socket within connection_function(). But for now, just this.
        """
        pass