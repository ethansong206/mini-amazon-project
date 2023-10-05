from flask import current_app as app

from .inventory import Inventory

class Product:
    def __init__(self, id, creator_id, name, category, description, image):
        self.pid = id
        self.creator_id = creator_id
        self.name = name
        self.category = category
        self.description = description
        self.image = image

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, creator_id, name, category, description, image
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(quantity):
        rows = app.db.execute('''
SELECT p.id, p.creator_id, p.name, p.category, p.description, p.image, i.price, i.quantity
FROM Products as p, Inventory as i
WHERE p.id = i.pid
AND p.creator_id = i.seller_id
AND i.quantity >= :quantity                                                        
''',
                              quantity=quantity)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_most_expensive(k):
        rows = app.db.execute('''
SELECT p.id, p.creator_id, p.name, p.category, p.description, p.image, i.price, i.quantity
FROM Products as p, Inventory as i
WHERE p.id = i.pid
AND p.creator_id = i.seller_id
ORDER BY i.price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]