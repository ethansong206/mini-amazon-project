from flask import current_app as app

class Inventory:
    def __init__(self, seller_id, pid, price, quantity):
        self.self = self
        self.seller_id = seller_id
        self.pid = pid
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT seller_id, pid, price, quantity
FROM Inventory
WHERE id = :id
''',
                              id=id)
        return Inventory(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_from_seller(seller_id):
        rows = app.db.execute('''
SELECT seller_id, pid, price, quantity, name
FROM Inventory
JOIN Products ON Products.id = pid
WHERE seller_id = :seller_id;
''',
                              seller_id=seller_id)
        return rows if rows else []

