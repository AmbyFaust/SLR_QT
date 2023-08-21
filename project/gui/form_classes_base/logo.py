import os

from PyQt5.QtGui import QIcon


GUI_RESOURCES_PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'resources'))
VECTOR_ALMAZ_ICON_PATH = os.path.join(GUI_RESOURCES_PATH, 'images', 'logo.svg')
RASTER_ALMAZ_ICON_PATH = os.path.join(GUI_RESOURCES_PATH, 'images', '_almaz_logo.png')
Q_ALMAZ_ICON = QIcon(VECTOR_ALMAZ_ICON_PATH)






