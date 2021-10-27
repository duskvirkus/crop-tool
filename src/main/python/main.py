# def parse_args():

#     parser = argparse.ArgumentParser()

#     control_window.ControlWindow.add_window_args(parser)
#     imqueue.ImQueue.add_im_queue_args(parser)

#     args = parser.parse_args()

#     return args

# def should_exit():

#     if editor.escaped:
#         return True

#     if not controls.keep_alive():
#         return True

#     return False

import sys

from application_controller import ApplicationController


def main():

    app_controller = ApplicationController()
    exit_code = app_controller.start()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()