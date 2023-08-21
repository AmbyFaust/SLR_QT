class ComplexObjectBase:
    """
    Базовый класс для комплексных объектов карты.
    Может быть использован вместе с классом ObjectBase.
    """
    def __init__(self):
        self.objects_dict = {}

    def draw(self, draw_hidden=False):
        self._draw_objects(list(self.objects_dict.keys()), draw_hidden)

    def set_visibility(self, visibility):
        self._set_visibility(list(self.objects_dict.keys()), visibility)

    def remove(self):
        self._remove_objects(list(self.objects_dict.keys()))

    def redraw(self):
        self._redraw_objects(list(self.objects_dict.keys()))

    # ---------------------------------------------------------------

    def _draw_objects(self, objects_id: list, draw_hidden):
        for key in objects_id:
            self.objects_dict[key].draw(draw_hidden)

    def _set_visibility(self, objects_id: list, visibility):
        for key in objects_id:
            self.objects_dict[key].set_visibility(visibility)

    def _remove_objects(self, objects_id: list):
        for key in objects_id:
            self.objects_dict[key].remove()

    def _redraw_objects(self, objects_id: list):
        for key in objects_id:
            self.objects_dict[key].redraw()
    # ---------------------------------------------------------------
