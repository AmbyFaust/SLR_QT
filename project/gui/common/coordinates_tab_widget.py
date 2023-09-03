from enum import Enum

from PyQt5.QtWidgets import QApplication, QTabWidget, QLabel, QVBoxLayout, QWidget

from project.gui.common.coordinates_translator import CoordinateSystemEpsg, translate_coordinates
from project.gui.mark_reviewer.coordinate_tabs import GeodesicTab, GeocentricTab
from project.gui.common import coordinates_translator


class CoordinatesTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.__create_widgets()
        self.coordinates = self.widget(self.currentIndex()).get_coordinates()
        self.cur_coordinates_system = self.widget(self.currentIndex()).get_coordinates_system()
        self.currentChanged.connect(self.on_tab_changed)

    def __create_widgets(self):
        # self.coordinates_tabs.currentChanged.connect(self.on_tab_changed)

        self.wgs_tab = GeodesicTab(CoordinateSystemEpsg.wgs_84)
        self.pz_tab = GeodesicTab(CoordinateSystemEpsg.pz_90)
        self.sk_tab = GeodesicTab(CoordinateSystemEpsg.sk_42)

        self.gauss_kruger_tab = GeocentricTab(CoordinateSystemEpsg.gauss_kruger)

        self.addTab(self.wgs_tab, 'WGS-84')
        self.addTab(self.pz_tab, 'ПЗ-90.11')
        self.addTab(self.sk_tab, 'СК-42')
        self.addTab(self.gauss_kruger_tab, 'Проекция Гаусса-Крюгера')

    def get_coordinates_cur_tab(self):
        if self.cur_coordinates_system == self.wgs_tab.get_coordinates_system():
            return self.wgs_tab.get_coordinates()
        elif self.cur_coordinates_system == self.pz_tab.get_coordinates_system():
            return self.pz_tab.get_coordinates()
        elif self.cur_coordinates_system == self.sk_tab.get_coordinates_system():
            return self.sk_tab.get_coordinates()
        elif self.cur_coordinates_system == self.gauss_kruger_tab.get_coordinates_system():
            return self.gauss_kruger_tab.get_coordinates()

    def set_coordinates_cur_tab(self):
        if self.cur_coordinates_system == self.wgs_tab.get_coordinates_system():
            self.wgs_tab.set_coordinates(*self.coordinates)
        elif self.cur_coordinates_system == self.pz_tab.get_coordinates_system():
            self.pz_tab.set_coordinates(*self.coordinates)
        elif self.cur_coordinates_system == self.sk_tab.get_coordinates_system():
            self.sk_tab.set_coordinates(*self.coordinates)
        elif self.cur_coordinates_system == self.gauss_kruger_tab.get_coordinates_system():
            self.gauss_kruger_tab.set_coordinates(*self.coordinates)

    def on_tab_changed(self, index):
        changed_coordinates_system = self.currentWidget().get_coordinates_system()
        changed_coordinates = self.get_coordinates_cur_tab()

        self.coordinates = list(translate_coordinates(
            self.cur_coordinates_system,
            changed_coordinates_system,
            (changed_coordinates[0], changed_coordinates[1])
        )) + [changed_coordinates[-1]]

        self.cur_coordinates_system = changed_coordinates_system
        self.set_coordinates_cur_tab()
