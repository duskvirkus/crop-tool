
import cv2
import numpy as np

from imqueue import ImQueue
from rect_data import RectData

class EditWindow:

    def __init__(
        self,
        queue: ImQueue,
    ) -> None:
        cv2.startWindowThread()
        cv2.namedWindow('Editor', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Editor', 1200,800)
        cv2.setMouseCallback('Editor', self.mouse)

        self.mode = 'rect'
        self.rect = None

        self.queue = queue

        self.draw_img = None
        self.update_image()

        self.escaped = False

    def __del__(self):
        cv2.destroyAllWindows()

    def update(self):
        k = cv2.waitKey(33)

        if k == 27: # esc
            self.escaped = True

        if k == 122: # z
            self.queue.back()
            self.update_image()

        if k == 120: # x
            self.queue.advance()
            self.update_image()

    def display(self):

        if self.draw_img is not None:
            cv2.imshow('Editor', self.draw_img)

    def update_image(self):
        img = self.queue.get_current_image()
        if img is not None:
            self.draw_img = img.copy()

            if self.rect is not None:
                self.draw_edit(self.rect, (255, 255, 0), (255, 0, 0), (0, 255, 0))
                


    def draw_edit(self, rect_data, color1, color2, color3):
        # rect = pre_process_rect(rect_data)

        cv2.rectangle(
            self.draw_img,
            rect_data.get1(),
            rect_data.get2(),
            color1,
            10
        )

        square = rect_data.get_square()
        cv2.rectangle(
            self.draw_img,
            square[0],
            square[1],
            color2,
            10
        )

        padded = rect_data.get_padded()
        cv2.rectangle(
            self.draw_img,
            padded[0],
            padded[1],
            color3,
            10
        )


    def reset(self):
        self.rect = None

    def save_edit(self):
        self.queue.add_edit(self.mode, self.rect)

    def mouse(self, event, x, y, flags, param):
        if(self.mode == 'rect'):
            self.rect_mouse(event, x, y, flags, param)

    def rect_mouse(self, event, x, y, flags, param):
        # print(event, x, y, flags, param)

        if self.rect is not None:
            self.rect.set2(x, y)
            self.update_image()

        if event==4: #CLICK UP
            if self.rect is None:
                self.rect = RectData(x, y)
            else:
                self.save_edit()
                self.reset()
