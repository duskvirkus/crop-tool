from imqueue import ImQueue
from edit_window import EditWindow

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from application_window import ApplicationWindow

class ApplicationController(ApplicationContext):

    def __init__(self) -> None:
        super().__init__()

        self.setup_done = False
        self.running = True

        self.app_window = ApplicationWindow(self)

        self.queue = None # imqueue.ImQueue(None)
        self.edit_window = None
        self.callback_update_table = None
        
    def __del__(self):
        self.queue.__del__()
        self.edit_window.__del__()

    def start(self):
        self.app_window.start()
        return self.app.exec()

    def update(self):
        if self.edit_window is not None:
            self.edit_window.update()
            self.edit_window.display()

        self.app_window.update()

    def set_callback_load_images(self, callback) -> None:
        self.callback_load_images = callback

    def load_images(self, dir: str) -> None:
        if not self.setup_done:
            self.queue = ImQueue(self)

        self.queue.add_directory(dir)

        if not self.setup_done:
            self.edit_window = EditWindow(self.queue)
            self.setup_done = True

        self.callback_load_images(self.queue)

    def next_image(self) -> None:
        if self.setup_done:
            self.queue.advance()