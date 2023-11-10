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
        return rows if rows else []

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
        return rows if rows else []
    
    @staticmethod
    def get_all_sellers(uid, pid):
        rows = app.db.execute('''
SELECT I.pid, I.seller_id, I.quantity, S.num_items, I.price
FROM Inventory AS I
LEFT JOIN (SELECT * FROM SavedItems WHERE uid=:uid) as S
ON I.pid = S.pid
AND I.seller_id = S.seller_id
WHERE I.pid = :pid
''',
                              uid=uid, pid=pid)
        # sellers = [row.creator_id for row in rows]
        return rows if rows else []
    
    @staticmethod
    def get_all_from_category(category):
        if category != "":
            rows = app.db.execute('''
SELECT id, creator_id, name, category, description, image
FROM Products
WHERE category = :category
''', 
                              category=category)
        else:
            rows = app.db.execute('''
SELECT id, creator_id, name, category, description, image
FROM Products
''')

        return rows if rows is not None else None
    
    @staticmethod
    def get_all_categories():
        rows = app.db.execute('''
SELECT DISTINCT(name)
FROM Category
''')

        return rows if rows is not None else None
    
    @staticmethod
    def search(text):
        rows = app.db.execute('''
SELECT id, creator_id, name, category, description, image
FROM Products
WHERE name ILIKE '%' || :text || '%' OR description ILIKE '%' || :text || '%'
''',
                              text=text)
        return rows if rows is not None else None
