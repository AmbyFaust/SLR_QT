import numpy


def create_polygon_points(*, latitude: float, longitude: float, radius: float,
                           points_count: int = 40, azimuth_1: float = 0, azimuth_2: float = 360) -> [(float, float)]:
    """
    : return: список кортежей (latitude, longitude) входные данные корректны, иначе возвращается None
    """
    if latitude is None or longitude is None or radius is None or radius <= 0 or points_count <= 0:
        return None
    a = 6378137.0
    σ = radius / a
    φ = numpy.radians(latitude)
    λ = numpy.radians(longitude)
    Α = numpy.radians(numpy.linspace(azimuth_1, azimuth_2, points_count))
    Φ = numpy.arcsin(numpy.sin(φ) * numpy.cos(σ) + numpy.cos(φ) * numpy.sin(σ) * numpy.cos(Α))
    Λ = λ * numpy.ones(len(Α)) + numpy.arctan(
        numpy.sin(σ) * numpy.sin(Α) / (numpy.cos(σ) * numpy.cos(φ) - numpy.sin(σ) * numpy.sin(φ) * numpy.cos(Α)))
    return [(numpy.degrees(Φ[i]), numpy.degrees(Λ[i])) for i in range(len(Α))]
