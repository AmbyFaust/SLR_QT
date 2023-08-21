from qgis.core import QgsRectangle

from typing import Tuple

from dataclasses import dataclass


@dataclass
class Extent:
    x_min: float
    y_max: float
    x_max: float
    у_min: float

    def center(self) -> Tuple[float, float]:
        x_center = (self.x_max - self.x_min) / 2.0 + self.x_min
        y_center = (self.y_max - self.у_min) / 2.0 + self.у_min
        return x_center, y_center

    def to_rectangle(self) -> QgsRectangle:
        return QgsRectangle(self.x_min, self.у_min, self.x_max, self.y_max)


def extent_from_rectangle(rect: QgsRectangle) -> Extent:
    return Extent(rect.xMinimum(), rect.yMaximum(), rect.xMaximum(), rect.yMinimum())


