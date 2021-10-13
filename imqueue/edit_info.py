import os
import abc

import numpy as np

import cv2

from im_queue_item import ImQueueItem
from im_format import ImFormat, formatToCVFormat, formatToString

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