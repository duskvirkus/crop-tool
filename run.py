import argparse

import gui
import imqueue

def parse_args():

    parser = argparse.ArgumentParser()

    gui.Window.add_window_args(parser)
    imqueue.ImQueue.add_im_queue_args(parser)

    args = parser.parse_args()

    return args

def main():

    global args
    global window
    global imqueue

    args = parse_args()

    window = gui.Window(vars(args))
    imqueue = imqueue.ImQueue(vars(args))

    while window.keep_alive():
        window.render_frame()

if __name__ == "__main__":
    main()