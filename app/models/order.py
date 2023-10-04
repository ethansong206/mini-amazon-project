from flask import current_app as app

from .purchase import Purchase

class Order:
    def __init__(self, id, uid, status, timestamp):
        self.id = id
        self.uid = uid
        self.status = status
        self.timestamp = timestamp

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, uid, status, timestamp
        FROM Orders
        WHERE id = :id
        ''', id=id)

        return Order(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT id, uid, status, timestamp
        FROM Orders
        WHERE uid = :uid
        AND timestamp >= :since
        ''', uid=uid, since=since)

        return [Order(*row) for row in rows]

    @staticmethod
    def submit()