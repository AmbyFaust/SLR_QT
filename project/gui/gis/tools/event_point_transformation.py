from ..canvas_transformer import canvas_transformer


def event_point_to_lat_lon(point):
    return canvas_transformer.x_y_to_lat_lon(x=point.x(), y=point.y())
