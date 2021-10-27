import sys
import os

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QWidget, QVBoxLayout, QHBoxLayout, QListView, QTextEdit
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from PyQt5.QtCore import QTimer
# from application_controller import ApplicationController

def get_default_out_dir() -> str:
    path = os.path.abspath(__file__)
    split_path = path.split('/')
    split_path = split_path[:-4]
    split_path.append('output')
    return '/'.join(split_path)

class ApplicationWindow(QMainWindow):

    def __init__(
        self,
        app_controller
    ) -> None:
        super().__init__()
        
        self.app_controller = app_controller

        self.app_controller.set_callback_load_images(self.populate_loaded_table)

        # self.window = QMainWindow()
        self.setWindowTitle('Crop Tool')
        self.resize(800, 600)

        # setup actions
        open_image_dir_action = QAction('Open Images Directory', self)
        open_image_dir_action.setShortcut('Ctrl+o')
        open_image_dir_action.setStatusTip('Open a folder of images.')
        open_image_dir_action.triggered.connect(self.open_images_dir)

        exit_action = QAction('Exit', self)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+z')
        undo_action.setStatusTip('Undo last crop on current image.')
        undo_action.triggered.connect(self.undo)

        preferences_action = QAction('Preferences...', self)
        preferences_action.setStatusTip('Modify application preferences.')
        preferences_action.triggered.connect(self.preferences)

        next_action = QAction('Next', self)
        next_action.setShortcut('x')
        next_action.setStatusTip('Proceed to next image.')
        next_action.triggered.connect(self.next)

        previous_action = QAction('Previous', self)
        previous_action.setShortcut('z')
        previous_action.setStatusTip('Go back to previous image.')
        previous_action.triggered.connect(self.next)

        # setup gui elements
        self.core_widget = QWidget()

        self.core_v_layout = QVBoxLayout()
        self.core_widget.setLayout(self.core_v_layout)

        # self.secondary_h_layout = QHBoxLayout()
        # self.secondary_h_layout.addStretch(0)
        # self.core_v_layout.addLayout(self.secondary_h_layout)

        self.out_dir_text_box = QTextEdit(get_default_out_dir())
        self.core_v_layout.addWidget(self.out_dir_text_box)

        # self.navigation = QHBoxLayout()

        self.loaded_list = QListView()
        self.core_v_layout.addWidget(self.loaded_list)

        # self.core_v_layout.addWidget(self.edit_panel)

        # self.use_gpu_checkbox = QCheckBox('Use GPU')
        # self.use_gpu_checkbox.setChecked(True)
        # self.navigation.addWidget(self.use_gpu_checkbox)

        # self.run_lpips = QtWidgets.QPushButton('Run lpips')
        # self.run_lpips.clicked.connect(self.run_lpips_func)
        # self.navigation.addWidget(self.run_lpips)

        # self.next_image = QPushButton('Next Image')
        # self.next_image.clicked.connect(self.next_image_func)
        # self.navigation.addWidget(self.next_image)

        # self.core_v_layout.addLayout(self.navigation)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_image_dir_action)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(undo_action)
        edit_menu.addAction(preferences_action)

        navigation_menu = menu_bar.addMenu('&Navigation')
        navigation_menu.addAction(next_action)
        navigation_menu.addAction(previous_action)

        # # setup edit grid and comparison list
        # self.controller.edit_grid.create_q_widgets()
        # self.controller.edit_grid.set_grid_parent(self.secondary_h_layout)
        # self.controller.comparison_list.create_q_widgets()
        # self.controller.comparison_list.set_parent(self.secondary_h_layout)

        # finish setting up gui
        self.setCentralWidget(self.core_widget)

        QTimer.singleShot(200, self.app_controller.update)
        # self.timer = QTimer(self)
        # connect(self.timer, QTimer.timeout, self, self.app_controller.update)
        # self.timer.start()

    def start(self) -> None:
        self.show()

    def update(self) -> None:
        self.update_loaded_table()
        QTimer.singleShot(200, self.app_controller.update)

    def open_images_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Images Directory')
        self.app_controller.load_images(dir_name)

    def undo(self):
        pass

    def next(self):
        self.app_controller.next_image()

    def preferences(self):
        pass

    def populate_loaded_table(self, queue):
        item_model = QStandardItemModel(self.loaded_list)
        for i in range(len(queue.items)):
            item = queue.items[i]
            qitem = QStandardItem(item.short_name())
            # qitem.setCheckable(True)
            # qitem.setCheckState(item.loaded())

            item_model.appendRow(qitem)

            # # selected_list[i] = imgui.selectable(item.gui_readout(), selected_list[i])
            # # imgui.text(item.short_name())
            # if imgui.is_item_hovered():
            #     imgui.set_tooltip(item.file_location)

        self.loaded_list.setModel(item_model)

    def update_loaded_table(self):
        if self.app_controller.queue is not None and self.loaded_list.model():
            assert(len(self.app_controller.queue.items) == self.loaded_list.model().rowCount()) # TODO generalize
            for i in range(len(self.app_controller.queue.items)):
                item = self.app_controller.queue.items[i]
                # qitem = self.loaded_list.model().item(i)

                qitem = QStandardItem(item.short_name())
                # qitem.setCheckable(True)
                icon_path = './src/main/assets/app_icons/image_not_loaded.png'
                if item.loaded():
                    icon_path = './src/main/assets/app_icons/image.png'
                qitem.setIcon(QIcon(icon_path))
                
                # qitem.setCheckState(item.loaded())

                self.loaded_list.model().setItem(i, qitem)
