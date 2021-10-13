from typing import Any
from enum import Enum
import abc
from argparse import ArgumentParser
import os

import cv2
import numpy as np


class ImFormat(Enum):
    PNG = 0,
    JPG = 1,

def formatToString(format: ImFormat) -> str:
    if format == ImFormat.PNG:
        return '.png'
    elif format == ImFormat.JPG:
        return '.jpg'
    raise Exception('Unknown format in formatToString().')

def formatToCVFormat(format: ImFormat):
    if format == ImFormat.PNG:
        return [cv2.IMWRITE_PNG_COMPRESSION, 0]
    elif format == ImFormat.JPG:
        return [cv2.IMWRITE_JPEG_QUALITY, 100]
    raise Exception('Unknown format in formatToCVFormat().')

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

    def current(self):
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
        parser.add_argument("--memory_max", help='Maximum amount of system memory to use when loading images in megabites. (default: %(default)s)', type=int, default=4096)
        parser.add_argument("--save_format", help='file extension ["png","jpg"] (default: %(default)s)', default='png')
        return parent_parser

class ImQueueItem:

    def __init__(
        self,
        queue: ImQueue,
        file_location: str,
    ):
        self.queue = queue
        self.file_location = file_location

        self.img = None
        self.edits = []
        self.edit_counter = 0

    def loaded(self) -> bool:
        return self.img is None

    def load(self) -> None:
        self.img = cv2.imread(self.file_location)

    def next_edit_id(self) -> int:
        edit_id = self.edit_counter
        self.edit_counter += 1
        return edit_id


class EditInfo(abc.ABC):

    def __init__(
        self,
        original: ImQueueItem,
        save_loc: str,
        file_prefix: str,
        edit_id: int,
    ):
        self.original = original
        self.save_loc = save_loc
        self.file_prefix = file_prefix
        self.edit_id = edit_id

        if os.isfile(self.isfile(self.save_path())):
            new_file_prefix = self.file_prefix + '-'
            print(f'Warning: {self.save_path()} already exists. Changing file_prefix to {new_file_prefix} to avoid collision.')
            self.file_prefix = new_file_prefix

    def saved(self) -> bool:
        return os.isfile(self.save_loc)

    def save(self):
        edited = self.apply_edit()
        cv2.imwrite(self.save_path, edited, formatToCVFormat(self.format()))

    def save_path(self):
        return os.path.join(self.save_loc, self.file_prefix + '-' + self.edit_id + formatToString(self.format()))

    def format(self) -> ImFormat:
        return self.original.queue.save_format

    def delete(self):
        if self.saved():
            os.remove(self.save_path())
        else:
            print(f'Warning: delete attempted on {self.save_path}, however file has not been saved yet.')

    @abc.abstractmethod
    def apply_edit(self) -> np.array:
        pass