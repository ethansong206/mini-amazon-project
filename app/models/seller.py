from flask import current_app as app

class Seller:
    def __init__(self, id):
        self.self = self
        self.id = id

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id
FROM Sellers
WHERE id = :id
''',
                              id=id)
        return Seller(*(rows[0])) if rows else None


    @staticmethod
    def get_orders(id):
        rows = app.db.execute('''
        SELECT *
        FROM Purchases Pur
        LEFT JOIN Products Pro
        ON Pur.pid = Pro.id
        WHERE seller_id=:id
        ORDER BY Pur.time_purchased DESC
        ''',
        id=id)

        return rows if rows else None