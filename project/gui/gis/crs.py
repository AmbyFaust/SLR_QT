from .canvas_transformer import canvas_transformer


project_crs = canvas_transformer.projection_srs  # служебная переменная


canvas_crs = project_crs        # СК канвы
sar_crs = project_crs           # СК, в которой отображаются РЛИ
map_fragment_crs = project_crs  # СК, в которой отображается фрагмент подложки под РЛИ
vector_crs = project_crs        # СК, в которой отображаются векторные объекты


def set_layer_crs(layer, crs):
    layer.setCrs(crs)
    layer.crs().postgisSrid()










