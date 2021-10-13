import cv2

from im_queue import ImQueue

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