class MarkData:
    """
        latitude и longitude - в системе СК-42
    """
    def __init__(self,
                 obj_id=None,
                 name=None,
                 datetime=None,
                 object_type=None,
                 relating_name=None,
                 relating_type=None,
                 latitude=None,
                 longitude=None,
                 altitude=None,
                 comment=None):
        self.obj_id = obj_id
        self.name = name
        self.datetime = datetime
        self.object_type = object_type
        self.relating_name = relating_name
        self.relating_type = relating_type
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.comment = comment

