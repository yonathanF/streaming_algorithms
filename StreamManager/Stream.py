"""
Stream Manager

Implements a basic observable pattern so that multiple streaming algorithms
can react to the data. Accepts a data generator.
"""

from queue import Queue, Empty
from threading import Thread

class SimpleStream:
    """
    A simple stream. Provides data at unspecified rate.
    """
    def __init__(self, data_source, buffer_size=100):
        self.data_source = data_source
        self.buffer_size = buffer_size
        self.buffer = Queue(buffer_size)
        self.subscribers = []

        self.notification_thread = Thread(target=self.notifier)
        self.notification_thread.start()
        self.producer_thread = Thread(target=self.fill_buffer)
        self.producer_thread.start()


    def shutdown(self):
        self.buffer.put(None)
        self.notification_thread.join()
        self.producer_thread.join()

    def is_buffer_full(self):
        return self.buffer.full()

    def notifier(self):
        while True:
            new_data = self.buffer.get()
            if new_data is None:
                break
            for subscriber in self.subscribers:
                subscriber(new_data)
            self.buffer.task_done()


    def subscribe(self, callback):
        """
        Adds a subscriber to the known subsribers

        :param callback: the function that will be called when new items arrive
        """
        self.subscribers.append(callback)

    def get(self):
        """
        Gets a single element from the stream

        .. warning:: This removes the item from the buffer
        """
        try:
            return self.buffer.get()
        except Empty:
            self.fill_buffer()
            return self.buffer.get()


    def fill_buffer(self):
        """
        Fills up the buffer using the data source
        """
        while True:
            data = self.data_source()
            if data is None:
                break
            self.buffer.put(data)
