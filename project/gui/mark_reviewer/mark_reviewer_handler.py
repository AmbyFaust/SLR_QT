from project.database.entities.ObjectEntity import ObjectEntity


class MarkReviewerHandler:
    @staticmethod
    def create_mark(x, y):
        mark_id = 1
        return mark_id

    @staticmethod
    def delete_mark(mark_id):
        pass

    @staticmethod
    def toggle_mark_visibility(mark_id, visibility):
        pass

    @staticmethod
    def update_database(object_id, mark_id, name, object_type, relating_object_id, meta):
        ObjectEntity.update_object(object_id, mark_id, name, object_type, relating_object_id, meta)

