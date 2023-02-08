from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
)
from PyQt5.QtGui import QPixmap, QKeyEvent

from static_maps_api import get_map
from window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self._map_zoom = 5
        self._map_ll = [37.977751, 55.757718]
        self._map_l = 'map'
        self._init_ui()

    def _init_ui(self) -> None:
        self._refresh_map()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        move_distance = 35 / self._map_zoom ** 2
        previous_zoom = self._map_zoom
        previous_ll = self._map_ll.copy()
        if event.key() == Qt.Key_PageUp:
            self._map_zoom += 1
        elif event.key() == Qt.Key_PageDown:
            self._map_zoom -= 1
        elif event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            self._map_ll[1] += move_distance
        elif event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            self._map_ll[0] -= move_distance
        elif event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            self._map_ll[0] += move_distance
        elif event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            self._map_ll[1] -= move_distance
        self._map_zoom = self._clip_zoom(self._map_zoom, 1, 16)
        if previous_zoom == self._map_zoom and previous_ll == self._map_ll:
            return
        self._refresh_map()

    def _clip_zoom(self, zoom: int, min_zoom: int, max_zoom: int) -> int:
        if zoom < min_zoom:
            return min_zoom
        if zoom > max_zoom:
            return max_zoom
        return zoom

    def _refresh_map(self) -> None:
        image_data = get_map(ll=self._map_ll, zoom=self._map_zoom, map_type=self._map_l)
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.map_label.setPixmap(pixmap)
