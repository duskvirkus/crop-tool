from gui.window import Window

def main():

    global window

    window = Window(1280, 720)

    while window.keep_alive():
        window.render_frame()

if __name__ == "__main__":
    main()