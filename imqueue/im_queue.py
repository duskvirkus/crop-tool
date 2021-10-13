from typing import Any
from argparse import ArgumentParser

from im_queue_item import ImQueueItem
from utils.im_queue import ImFormat

class ImQueue:

    def __init__(
        self,
        kwargs: Any,
    ):
        self.load_directories = kwargs['load_directories']
        self.memory_max = kwargs['memory_max']
        self.save_format: ImFormat = kwargs['save_format']
        
        self.items = []
        self.queue_position = 0
        self.populate_queue()

    def populate_queue(self) -> None:
        pass

    def current(self) -> ImQueueItem:
        return self.items[self.queue_position]

    def advance(self) -> bool:
        if len(self.items) >= self.queue_position + 1:
            return False
        self.queue_position += 1
        return True

    def go_back(self) -> bool:
        if self.queue_position - 1 <= 0:
            return False
        self.queue_position -= 1
        return True

    @staticmethod
    def add_im_queue_args(parent_parser: ArgumentParser) -> ArgumentParser:
        parser = parent_parser.add_argument_group("ImQueue Args")
        parser.add_argument("-i", "--input_directories", help='Directories to load images from. Formated in paths seperated by spaces.', type=str, required=True)
        parser.add_argument("--memory_max", help='Maximum amount of system memory to use when loading images in megabites. ', type=int, default=4096)
        parser.add_argument("--save_format", help='file extension ["png","jpg"] (default: %(default)s)', default='png')
        return parent_parser