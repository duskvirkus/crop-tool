from argparse import ArgumentParser
from typing import Any

import glfw
import imgui

import OpenGL.GL as gl

from imgui.integrations.glfw import GlfwRenderer

class ControlWindow:

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

    def render_frame(self, queue, update_callback) -> None:
        glfw.poll_events()
        self.impl.process_inputs()

        imgui.new_frame()

        gl.glClearColor(0., 0., 0., 1.)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.file_list(queue, update_callback)

        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)


    def file_list(self, queue, update_callback):

        imgui.begin("queue list")

        imgui.listbox_header("", 400, 600)

        selected_list = [i == queue.queue_position for i in range(len(queue.items))]

        for i in range(len(queue.items)):
            item = queue.items[i]
            _, selected_list[i] = imgui.selectable(item.gui_readout(), selected_list[i])
            # imgui.text(item.short_name())
            if imgui.is_item_hovered():
                imgui.set_tooltip(item.file_location)
            # imgui.next_column()
            # imgui.text(str(item.loaded()))
            # imgui.next_column()

        # imgui.selectable("Selected", True)
        # imgui.selectable("Not Selected", False)

        print(selected_list)

        for i in range(len(selected_list)):
            if selected_list[i] and i != queue.queue_position:
                queue.set_position(i)
                update_callback()

        imgui.listbox_footer()

        imgui.end()

        # imgui.begin("")
        # imgui.columns(2, 'fileList')
        # imgui.text("File")
        # imgui.next_column()
        # imgui.text("Loaded?")
        # imgui.next_column()

        # for i in range(len(queue.items)):
        #     item = queue.items[i]
        #     imgui.text(item.short_name())
        #     if imgui.is_item_hovered():
        #         imgui.set_tooltip(item.file_location)
        #     imgui.next_column()
        #     imgui.text(str(item.loaded()))
        #     imgui.next_column()


        # imgui.columns(1)
        # imgui.end()

    @staticmethod
    def add_window_args(parent_parser: ArgumentParser) -> ArgumentParser:
        parser = parent_parser.add_argument_group("Window Args")
        parser.add_argument("--width", help='Starting window width. (default: %(default)s)', type=int, default=400)
        parser.add_argument("--height", help='Starting window height. (default: %(default)s)', type=int, default=720)
        return parent_parser
