
import cv2
import numpy as np

from imqueue import ImQueue

class EditWindow:

    def __init__(
        self,
        queue: ImQueue,
    ) -> None:
        cv2.startWindowThread()
        cv2.namedWindow('Editor', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Editor', 1200,800)
        self.queue = queue

        self.temp_img = None
        self.update_image()

        self.escaped = False

    def __del__(self):
        cv2.destroyAllWindows()

    def update(self):
        k = cv2.waitKey(33)
        # print(k)

        if k == 27: # esc
            self.escaped = True

    def display(self):

        cv2.imshow('Editor', self.temp_img)

    def update_image(self):
        img = self.queue.get_current_image()
        if img is not None:
            self.temp_img = img.copy()
