import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QToolBar, QAction, QGroupBox,
                             QLabel, QLineEdit, QComboBox, QCheckBox)

from project.singletons import journal
from project.settings import MAIN_RASTER_MAP_PATH

from project.gui import shortcuts, share
from project.gui.common import coordinates_translator as view_translator
from project.gui.common import DegreesMode, dd2dms, COMBOBOX_FONT, CHECKBOX_FONT
from project.gui.generated import resources

from .canvas_widget import CanvasWidget
from .canvas_painter import CanvasPainter
from .canvas_maps_manager import CanvasMapsManager
from .canvas_transformer import canvas_transformer
from .tools import CanvasRulerTool
from .maps_cacher import MapsCacher
from .drawable_objects import MarkAreaDrawable


class NoHiddenToolbar(QToolBar):
    def contextMenuEvent(self, a0) -> None:
        a0.ignore()

    def hideEvent(self, a0) -> None:
        self.setVisible(True)


class GisWindow(QMainWindow):

    DEFAULT_MAIN_MAP_VISIBILITY = True

    def __init__(self, parent=None):
        super(GisWindow, self).__init__(parent)
        self.map_first_show = not self.DEFAULT_MAIN_MAP_VISIBILITY
        self.current_map_path = ''
        self.first_map = True

        self.__create_map_tools()
        self.__create_widgets()
        self.__create_actions()
        self.__create_tool_bar()
        self.__create_layout()

        self.init_maps()

    def init_maps(self):
        try:
            if self.current_map_path != MAIN_RASTER_MAP_PATH and self.first_map is False:
                self.maps_manager.remove_raster_fragment(CanvasMapsManager.MAIN_MAP_KEY)

            self.first_map = False
            self.current_map_path = MAIN_RASTER_MAP_PATH

            if os.path.exists(self.current_map_path):
                map_cacher = MapsCacher()
                map_cacher.map_is_cached.connect(self.__init_maps)
                map_cacher.cache_map(self.current_map_path)

        except BaseException as exp:
            print(exp)

    def __init_maps(self, map_path):
        if map_path != self.current_map_path:
            return
        self.maps_manager.add_main_map(self.current_map_path, self.main_map_visibility_checkbox.isChecked())
        self.canvas.original_state()

    def __create_map_tools(self):
        self.maps_manager = CanvasMapsManager()

        self.canvas = CanvasWidget()
        self.painter = CanvasPainter(self.canvas, self.maps_manager)

        # сигнал о координатах под курсором
        self.canvas.xyCoordinates.connect(self.__update_coordinates_widgets)

        # сигнал об изменении видимости карты
        self.maps_manager.maps_visibility_changed.connect(self.painter.visible_maps_changed_slot)
        self.painter.visible_maps_changed_slot()

        # первоначальное центрирование к подложке
        if self.DEFAULT_MAIN_MAP_VISIBILITY:
            self.canvas.original_state()

        # инструмент "линейка"
        self.ruler_tool = CanvasRulerTool(self.painter, color=QColor(Qt.red))
        self.ruler_tool.cancelled.connect(self.__ruler_deactivated)
        self.ruler_tool.finished.connect(self.__ruler_deactivated)

        # пользовательская отметка области
        self.area_mark = None

    def __create_widgets(self):
        self.main_map_visibility_checkbox = QCheckBox('Показывать подложку')
        self.main_map_visibility_checkbox.setCheckState(Qt.Checked if self.DEFAULT_MAIN_MAP_VISIBILITY is True else Qt.Unchecked)
        self.main_map_visibility_checkbox.setFont(CHECKBOX_FONT)
        self.main_map_visibility_checkbox.clicked.connect(self.__main_map_visibility_checkbox_checked)

        self.mark_x_label = QLabel('X (ГСК):')
        self.mark_x_gsk_lineEdit = QLineEdit()
        self.mark_x_gsk_lineEdit.setInputMask('9999999')
        self.mark_x_gsk_lineEdit.setMaxLength(8)
        self.mark_x_gsk_lineEdit.setMaximumWidth(70)

        self.mark_y_label = QLabel('Y (ГСК):')
        self.mark_y_gsk_lineEdit = QLineEdit()
        self.mark_y_gsk_lineEdit.setInputMask('9999999')
        self.mark_y_gsk_lineEdit.setMaxLength(8)
        self.mark_y_gsk_lineEdit.setMaximumWidth(70)

        self.mark_visibility_checkbox = QCheckBox('Показывать метку')
        self.mark_visibility_checkbox.setFont(CHECKBOX_FONT)
        self.mark_visibility_checkbox.clicked.connect(self.__mark_visibility_checkbox_clicked)

        # self.generate_report_button =

        self.main_group_box = QGroupBox()

        self.degrees_mode_combobox = QComboBox()
        self.degrees_mode_combobox.setFont(COMBOBOX_FONT)
        self.degrees_mode_combobox.addItems(
            [DegreesMode.comment(DegreesMode.divided), DegreesMode.comment(DegreesMode.real)]
        )
        
        self.crs_mode_combobox = QComboBox()
        self.crs_mode_combobox.setFont(COMBOBOX_FONT)
        self.crs_mode_combobox.addItem(
            view_translator.CoordinateSystemEpsg.wgs_84.get_name(), view_translator.CoordinateSystemEpsg.wgs_84
        )
        self.crs_mode_combobox.addItem(
            view_translator.CoordinateSystemEpsg.pz_90.get_name(), view_translator.CoordinateSystemEpsg.pz_90
        )
        self.crs_mode_combobox.addItem(
            view_translator.CoordinateSystemEpsg.sk_42.get_name(), view_translator.CoordinateSystemEpsg.sk_42
        )
        self.crs_mode_combobox.addItem(
            view_translator.CoordinateSystemEpsg.gauss_kruger.get_name(), view_translator.CoordinateSystemEpsg.gauss_kruger
        )
        self.crs_mode_combobox.currentIndexChanged.connect(self.__crs_mode_changed)

        self.latitude_label = QLabel('Широта:')
        self.longitude_label = QLabel('Долгота:')

        self.latitude_line_edit = QLineEdit()
        self.latitude_line_edit.setReadOnly(True)

        self.longitude_line_edit = QLineEdit()
        self.longitude_line_edit.setReadOnly(True)

    def __create_layout(self):
        coordinates_hb_layout = QHBoxLayout()
        coordinates_hb_layout.addWidget(self.crs_mode_combobox)
        coordinates_hb_layout.addWidget(QLabel('  '))
        coordinates_hb_layout.addWidget(self.latitude_label)
        coordinates_hb_layout.addWidget(self.latitude_line_edit)
        coordinates_hb_layout.addWidget(self.longitude_label)
        coordinates_hb_layout.addWidget(self.longitude_line_edit)
        coordinates_hb_layout.addWidget(QLabel('  '))
        coordinates_hb_layout.addWidget(self.degrees_mode_combobox)

        group_box_vb_layout = QVBoxLayout()
        group_box_vb_layout.addWidget(self.canvas)
        group_box_vb_layout.addLayout(coordinates_hb_layout)
        self.main_group_box.setLayout(group_box_vb_layout)

        self.setCentralWidget(self.main_group_box)

    def __create_actions(self):
        self.original_state_action = QAction()
        self.original_state_action.setText("Начальный вид")
        self.original_state_action.setIcon(QIcon(":/images/full.svg"))
        self.original_state_action.triggered.connect(self.canvas.original_state)

        self.ruler_action = QAction()
        self.ruler_action.setText('Линейка')
        self.ruler_action.setIcon(QIcon(":/images/ruler.svg"))
        self.ruler_action.setShortcut(shortcuts.RULER_SHORTCUT)
        self.ruler_action.triggered.connect(self.__ruler_action_triggered)

        self.make_mark_action = QAction()
        self.make_mark_action.setText('Найти точку')
        self.make_mark_action.setIcon(QIcon(":/images/full.svg"))
        self.make_mark_action.triggered.connect(self.__mark_action_triggered)

    def __create_tool_bar(self):
        self.tool_bar = NoHiddenToolbar('Инструменты карты')
        self.tool_bar.setContextMenuPolicy(Qt.NoContextMenu)
        self.tool_bar.setMovable(False)
        self.addToolBar(self.tool_bar)

        self.tool_bar.addAction(self.original_state_action)
        self.tool_bar.addSeparator()

        self.tool_bar.addAction(self.ruler_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.main_map_visibility_checkbox)

        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.mark_x_label)
        self.tool_bar.addWidget(self.mark_x_gsk_lineEdit)
        self.tool_bar.addWidget(self.mark_y_label)
        self.tool_bar.addWidget(self.mark_y_gsk_lineEdit)
        self.tool_bar.addAction(self.make_mark_action)
        self.tool_bar.addWidget(self.mark_visibility_checkbox)

    def __main_map_visibility_checkbox_checked(self, checked: bool):
        self.maps_manager.set_main_map_visibility(checked)
        if self.map_first_show:
            self.map_first_show = False
            self.canvas.original_state()

    def __update_coordinates_widgets(self, position):
        # географические координаты
        latitude, longitude = canvas_transformer.x_y_to_lat_lon(x=position.x(), y=position.y())

        x_val, y_val = longitude, latitude
        srs_id = canvas_transformer.get_geographic_srs_id()  # откуда переводим
        cs = self.crs_mode_combobox.itemData(self.crs_mode_combobox.currentIndex(), Qt.UserRole)  # куда переводим

        x, y = view_translator.translate_coordinates(srs_id, cs, (x_val, y_val))  # результат перевода

        # если нужно показывать географические координаты
        if cs is not view_translator.CoordinateSystemEpsg.gauss_kruger:
            deg_mode = DegreesMode.mode_by_num(self.degrees_mode_combobox.currentIndex())
            if deg_mode is DegreesMode.real:
                self.latitude_line_edit.setText(f'{y:.6f}')
                self.longitude_line_edit.setText(f'{x:.6f}')
            else:
                self.latitude_line_edit.setText('{}°{}\'{:.2f}\'\''.format(*dd2dms(y)))
                self.longitude_line_edit.setText('{}°{}\'{:.2f}\'\''.format(*dd2dms(x)))
        # если нужно показывать координаты в проекции
        else:
            self.latitude_line_edit.setText(f'{x:.0f} м')  # потому что на форме сначала этот виджет
            self.longitude_line_edit.setText(f'{y:.0f} м')

    def __ruler_action_triggered(self):
        if not share.TOOLS_ACTIVITY:
            self.ruler_tool.start()
            share.TOOLS_ACTIVITY = True

    def __mark_action_triggered(self):
        try:
            x = float(self.mark_x_gsk_lineEdit.text())
            y = float(self.mark_y_gsk_lineEdit.text())
            src_epsg = view_translator.CoordinateSystemEpsg.gauss_kruger
            dst_epsg = view_translator.CoordinateSystemEpsg.wgs_84
            lon_wgs, lat_wgs = view_translator.translate_coordinates(src_epsg, dst_epsg, (x, y))
            mark_visibility = (self.mark_visibility_checkbox.checkState() == Qt.Checked)
            if self.area_mark is not None:
                self.area_mark.remove()
            self.area_mark = MarkAreaDrawable(self.painter, lat_wgs, lon_wgs)
            self.area_mark.draw(draw_hidden=not mark_visibility)
            self.area_mark.zoom_to_object()

        except BaseException as exp:
            journal.log(f'Не удалось сформировать отметку на карте. {exp}', attr='error')

    def __mark_visibility_checkbox_clicked(self, checked: bool):
        if self.area_mark is not None:
            self.area_mark.set_visibility(checked)

    @staticmethod
    def __ruler_deactivated():
        share.TOOLS_ACTIVITY = False

    def __crs_mode_changed(self, index):
        cs = self.crs_mode_combobox.itemData(index, Qt.UserRole)  # куда переводим
        if cs is view_translator.CoordinateSystemEpsg.gauss_kruger:
            self.latitude_label.setText('X:')
            self.longitude_label.setText('Y:')
            self.degrees_mode_combobox.setEnabled(False)
        else:
            self.latitude_label.setText('Широта:')
            self.longitude_label.setText('Долгота:')
            self.degrees_mode_combobox.setEnabled(True)

