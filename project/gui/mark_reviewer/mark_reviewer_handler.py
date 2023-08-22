import sqlite3


class Mark:
    def __init__(self):
        pass


class MarkHandler:
    def __init__(self):
        self.marks = []

    def add_mark(self, mark):
        self.marks.append(mark)


class MarkReviewerHandler:
    def __init__(self):
        pass

    def create_mark(self):
        pass

    def delete_mark(self):
        pass

    def update_mark(self):
        pass

    def toggle_mark_visibility(self):
        pass
