import copy

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit

from .degrees_mode import dd2dms, dms2dd


class DividedLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(DividedLineEdit, self).__init__(*args, **kwargs)
        degree_regexp = QtCore.QRegExp('(-)?([0-9]?[0-9]|1[0-7][0-9])°([0-5]?[0-9])\'([0-5]?[0-9])\'\'')
        self.setValidator(QtGui.QRegExpValidator(degree_regexp, self))
        self.setInputMask('00°00\'00\'\'')

    def set_value(self, value: float):
        d, m, s = dd2dms(value)
        self.setText(f'{d}°{m}\'{s}\'\'')

    def get_value(self) -> float:
        text = self.text()
        try:
            d_split = copy.deepcopy(text).split('°')
            if len(d_split) == 0:
                d = 0
            elif d_split[0] == '' or d_split[0] is None:
                d = 0
            else:
                d = int(d_split[0])

            m_split = copy.deepcopy(d_split[1]).split('\'')
            if len(m_split) < 1:
                m = 0
            elif m_split[0] == '' or m_split[0] is None:
                m = 0
            else:
                m = int(m_split[0])

            s_split = copy.deepcopy(m_split[1]).split('\'\'')
            if len(s_split) < 1:
                s = 0
            elif s_split[0] == '' or s_split[0] is None:
                s = 0
            else:
                s = int(s_split[0])
        except BaseException as exp:
            print(f'Исключение в файле {__file__}. {exp}')
            d, m, s = 0, 0, 0

        return dms2dd(d, m, s)
