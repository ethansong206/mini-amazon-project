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


