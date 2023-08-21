import math

from enum import Enum


class DegreesMode(Enum):
    divided = 0
    real = 1

    @staticmethod
    def mode_by_num(num: int):
        if num == 0:
            return DegreesMode.divided
        if num == 1:
            return DegreesMode.real
        return num

    def comment(self) -> str:
        return 'градусы' if self.value == 1 else 'градусы, минуты, секунды'


def dd2dms(deg: float) -> (int, int, int):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return d, m, sd


def dms2dd(d: int, m: int, sd: int) -> float:
    sign = math.copysign(1, d)
    return d + sign * (m / 60) + sign * (sd / 3600)
    # return d + (m / 60) + (sd / 3600)
