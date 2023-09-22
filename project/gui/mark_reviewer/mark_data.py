class MarkData:
    """
        latitude и longitude - в системе СК-42
    """
    def __init__(self,
                 obj_id=None,
                 name=None,
                 datetime=None,
                 object_type=None,
                 relating_type=None,
                 longitude=None,
                 latitude=None,
                 altitude=None,
                 comment=None):
        self.obj_id = obj_id
        self.name = name
        self.datetime = datetime
        self.object_type = object_type
        self.relating_type = relating_type
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.comment = comment

