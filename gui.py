from argparse import ArgumentParser
from typing import Any

import glfw
import imgui

import OpenGL.GL as gl

from imgui.integrations.glfw import GlfwRenderer

class Window:

    def __init__(
        self,
        kwargs: Any,
        window_name: str = 'Crop Tool',
    ):
        imgui.create_context()

        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        self.window = glfw.create_window(
            kwargs['width'],
            kwargs['height'],
            window_name,
            None,
            None
        )
        glfw.make_context_current(self.window)

        if not self.window:
            glfw.terminate()
            print("Could not initialize Window")
            exit(1)

        self.impl = GlfwRenderer(self.window)

    def keep_alive(self) -> bool:
        return not glfw.window_should_close(self.window)

    def render_frame(self) -> None:
        glfw.poll_events()
        self.impl.process_inputs()

        imgui.new_frame()

        gl.glClearColor(0., 0., 0., 1.)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)

    @staticmethod
    def add_window_args(parent_parser: ArgumentParser) -> ArgumentParser:
        parser = parent_parser.add_argument_group("Window Args")
        parser.add_argument("--width", help='Starting window width. (default: %(default)s)', type=int, default=1280)
        parser.add_argument("--height", help='Starting window height. (default: %(default)s)', type=int, default=720)
        return parent_parser
