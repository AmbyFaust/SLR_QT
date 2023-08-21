import typing
import math

from enum import Enum

from qgis.core import QgsPointXY, QgsCoordinateTransform, QgsCoordinateReferenceSystem


class CoordinateSystemEpsg(Enum):
    wgs_84 = 4326          # WGS-84, (широта, долгота)
    pz_90 = 7680           # ПЗ-90.11, (широта, долгота)
    sk_42 = 4284           # СК-42, (широта, долгота)
    world_mercator = 3395  # WGS 84 / World Mercator - EPSG:3395
    gauss_kruger = -1      # ФИКТИВНЫЙ ИДЕНТИФИКАТОР. Перевод в/из ГСК осуществляется особым способом

    def get_name(self) -> str:
        if self is CoordinateSystemEpsg.wgs_84:
            return 'WGS-84 (географ.)'
        if self is CoordinateSystemEpsg.pz_90:
            return 'ПЗ-90.11 (географ.)'
        if self is CoordinateSystemEpsg.sk_42:
            return 'СК-42 (географ.)'
        if self is CoordinateSystemEpsg.gauss_kruger:
            return 'Проекция Гаусса-Крюгера'
        return ''

    
def __to_gaus_kruger(src_crs: typing.Union[CoordinateSystemEpsg, int], coordinates: typing.Tuple[float, float]) -> typing.Tuple[float, float]:
    """
    На вход подается исходная СК и точка с 2-мя координатами.
    Если на входе географическая СК, то это долгота и широта соответственно.
    Если на входе проекция, то это x и y соответственно.
    На выходе x и y в проекции Гаусса-Крюгера, в метрах.
    """
    if isinstance(src_crs, CoordinateSystemEpsg):
        q_src_crs = QgsCoordinateReferenceSystem.fromEpsgId(src_crs.value)
    else:  # задаем через srs_id
        q_src_crs = QgsCoordinateReferenceSystem.fromSrsId(src_crs)
        
    # Если исходная СК не СК-42, то переводим сначала в нее
    sk_42_qcrs = QgsCoordinateReferenceSystem.fromEpsgId(CoordinateSystemEpsg.sk_42.value)
    if q_src_crs.srsid() != sk_42_qcrs.srsid():
        tr = QgsCoordinateTransform()
        tr.setSourceCrs(q_src_crs)
        tr.setDestinationCrs(sk_42_qcrs)
        point = tr.transform(QgsPointXY(*coordinates))  # точка в СК-42 (долгота и широта в градусах)
    else:
        point = QgsPointXY(*coordinates)  # точка в СК-42 (долгота и широта в градусах)
        
    # --------------------------- Перевод в проекцию Гаусса-Крюгера (ГОСТ 32453-2013) ------------------------------- 
    L_deg = point.x()  # долгота в градусах
    B_rad = math.radians(point.y())  # широта в радианах
    
    oneSixth = 1.0/6.0
    n = int(( 6.0 + L_deg ) * oneSixth)  # номер шестиградусной зоны    (28)

    one57 = 1.0/57.29577951
    l = ( L_deg - ( 3 + 6 * ( n - 1 ) ) ) * one57  # расстояние от точки до осевого меридиана зоны в радианной мере   (27)
    l2 = l*l
    sin_B = math.sin( B_rad )
    sin2_B = sin_B * sin_B
    sin4_B = sin2_B * sin2_B
    sin6_B = sin2_B * sin4_B

    x_gsk = 6367558.4968 * B_rad - math.sin(2.0*B_rad) * ( 16002.89 + 66.9607 * sin2_B + 0.3515 * sin4_B
             - l2 * ( 1594561.25 + 5336.535 * sin2_B + 26.790 * sin4_B + 0.149 * sin6_B
             + l2 * ( 672483.4 - 811219.9 * sin2_B + 5420.0 * sin4_B - 10.6 * sin6_B
             + l2 * ( 278194.0 - 830174.0 * sin2_B + 572434.0 * sin4_B - 16010.0 * sin6_B
             + l2 * ( 109500.0 - 574700.0 * sin2_B + 863700.0 * sin4_B - 398600.0 * sin6_B ) ) ) ) )   # (25)

    y_gsk = ( 5 + 10 * n ) * 1e5 + l * math.cos(B_rad) * ( 6378245.0 + 21346.1415 * sin2_B + 107.1590 * sin4_B + 0.5977 * sin6_B
             + l2 * ( 1070204.16 - 2136826.66 * sin2_B + 17.98 * sin4_B - 11.99 * sin6_B
             + l2 * ( 270806.0 - 1523417.0 * sin2_B + 1327645.0 * sin4_B - 21701.0 * sin6_B
             + l2 * ( 79690.0 - 866190.0 * sin2_B + 1730360.0 * sin4_B - 945460.0 * sin6_B ) ) ) )     # (26)
    # ----------------------------------------------------------------------------------------------------------------
    
    return x_gsk, y_gsk
    

def __from_gauss_kruger(x_gsk, y_gsk, dst_crs: CoordinateSystemEpsg) -> typing.Tuple[float, float]:
    """
    На вход подается координаты X и Y точки в проекции Гаусса-Крюгера в метрах.
    Если на выходе географическая СК, то это долгота и широта соответственно.
    Если на выходе проекция, то это x и y соответственно.
    
    Вначале координаты точки переводятся в CК-42, затем уже в целевую СК
    """
    
    # ------------------- Перевод в координат точки проекции Гаусса-Крюгера в СК-42 (ГОСТ 32453-2013) ----------------
    n = int(y_gsk * 1e-6)                #  (31)

    one6e6 = 1.0/6367558.4968
    betta = x_gsk * one6e6      #  (35)
    sin_betta = math.sin( betta )
    sin2_betta = sin_betta * sin_betta
    sin4_betta = sin2_betta * sin2_betta
    Bo = betta + math.sin(2*betta) * ( 0.00252588685 - 0.0000149186 * sin2_betta + 0.00000011904 * sin4_betta )    #  (32) Смотри также поправку к ГОСТУ
    sin_Bo = math.sin( Bo )
    sin2_Bo = sin_Bo * sin_Bo
    sin4_Bo = sin2_Bo * sin2_Bo
    sin6_Bo = sin2_Bo * sin4_Bo
    zo = ( y_gsk - ( 10 * n + 5 ) * 1e5 ) / ( 6378245.0 * math.cos( Bo ) )     #  (36)
    zo2 = zo * zo

    dB = - zo2 * math.sin(2.0*Bo) * ( 0.251684631 - 0.003369263 * sin2_Bo + 0.000011276 * sin4_Bo         #  Смотри также поправку к ГОСТУ
                    - zo2 * ( 0.10500614 - 0.04559916 * sin2_Bo + 0.00228901 * sin4_Bo - 0.00002987 * sin6_Bo
                    - zo2 * ( 0.042858 - 0.025318 * sin2_Bo + 0.014346 * sin4_Bo - 0.001264 * sin6_Bo
                    - zo2 * ( 0.01672 - 0.0063 * sin2_Bo + 0.01188 * sin4_Bo - 0.00328 * sin6_Bo ) ) ) )       #  (33)

    l = zo * ( 1.0 - 0.0033467108 * sin2_Bo - 0.0000056002 * sin4_Bo - 0.0000000187 * sin6_Bo
                   - zo2 * ( 0.16778975 + 0.16273586 * sin2_Bo - 0.0005249 * sin4_Bo - 0.00000846 * sin6_Bo
                   - zo2 * ( 0.0420025 + 0.1487407 * sin2_Bo + 0.005942 * sin4_Bo - 0.000015 * sin6_Bo
                   - zo2 * ( 0.01225 + 0.09477 * sin2_Bo + 0.03282 * sin4_Bo - 0.00034 * sin6_Bo
                   - zo2 * ( 0.0038 + 0.0524 * sin2_Bo + 0.0482 * sin4_Bo + 0.0032 * sin6_Bo ) ) ) ) )         #  (34)

    latitude_rad = Bo + dB   #  (29)

    one57 = 1.0/57.29577951
    
    longitude_rad = 6 * ( n - 0.5 ) * one57 + l     #  (30)

    # ----------------------------------------------------------------------------------------------------------------
    
    lon_deg = math.degrees(longitude_rad)
    lat_deg = math.degrees(latitude_rad)
    
    tr = QgsCoordinateTransform()  # преобразование
    tr.setSourceCrs(QgsCoordinateReferenceSystem.fromEpsgId(CoordinateSystemEpsg.sk_42.value))  # откуда
    tr.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(dst_crs.value))  # куда
    
    # перевод координат
    point = tr.transform(QgsPointXY(lon_deg, lat_deg))
    return point.x(), point.y()


def translate_coordinates(src_crs: typing.Union[CoordinateSystemEpsg, int],
                          dst_crs: CoordinateSystemEpsg,
                          coordinates: typing.Tuple[float, float]) -> typing.Tuple[float, float]:
    """
    На вход подается точка с 2-мя координатами.
    Если на входе географическая СК, то это долгота и широта соответственно.
    Если на входе проекция, то это x и y соответственно.
    На выходе аналогично входу.
    
    Работа с проекцией Гаусса-Крюгера осуществляется особым способом
    (перевод можно осуществлять только в проекцию, не наоборот + отдельная функция для перевода)
    """
    
    # Перевод в проекцию Гаусса-Крюгера -------------------------
    if dst_crs is CoordinateSystemEpsg.gauss_kruger:
        try:
            return __to_gaus_kruger(src_crs, coordinates)
        except BaseException as exp:
            print(f'Произошла КРИТИЧЕСКАЯ ОШИБКА при переводе координат в проекцию Гаусса-Крюгера: {exp}')
            return 0, 0
    # -----------------------------------------------------------
    
    # Перевод из проекции Гаусса-Крюгера -------------------------
    if isinstance(src_crs, CoordinateSystemEpsg):
        if src_crs is CoordinateSystemEpsg.gauss_kruger:
            try:
                return __from_gauss_kruger(*coordinates, dst_crs)
            except BaseException as exp:
                print(f'Произошла КРИТИЧЕСКАЯ ОШИБКА при переводе координат из проекции Гаусса-Крюгера: {exp}')
                return 0, 0
    # -----------------------------------------------------------
    
    # Типовой перевод координат (используя БД СК, встроенную в QGIS) --
    
    tr = QgsCoordinateTransform()
    # откуда
    if isinstance(src_crs, CoordinateSystemEpsg):
        q_src_crs = QgsCoordinateReferenceSystem.fromEpsgId(src_crs.value)
    else:  # задаем через srs_id
        q_src_crs = QgsCoordinateReferenceSystem.fromSrsId(src_crs)
        
    tr.setSourceCrs(q_src_crs)

    # куда
    tr.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(dst_crs.value))
    
    # перевод координат
    point = tr.transform(QgsPointXY(*coordinates))
    return point.x(), point.y()


