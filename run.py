import argparse
import time

import control_window
import edit_window
import imqueue

def parse_args():

    parser = argparse.ArgumentParser()

    control_window.ControlWindow.add_window_args(parser)
    imqueue.ImQueue.add_im_queue_args(parser)

    args = parser.parse_args()

    return args

def should_exit():

    if editor.escaped:
        return True

    if not controls.keep_alive():
        return True

    return False

def main():

    global args

    global controls
    global editor
    global imqueue

    args = parse_args()

    controls = control_window.ControlWindow(vars(args))
    imqueue = imqueue.ImQueue(vars(args))

    # wait for first image to load
    while not imqueue.items[0].loaded():
        # print('loading first image ...')
        time.sleep(1)

    editor = edit_window.EditWindow(imqueue)

    while not should_exit():

        controls.render_frame(imqueue, editor.update_image)
        editor.update()
        editor.display()

    imqueue.__del__()
    editor.__del__()

    exit(0)

if __name__ == "__main__":
    main()