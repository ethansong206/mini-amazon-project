from flask import current_app as app

from .order import Order

class Purchase:
    def __init__(self, order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated):
        self.order_id = order_id
        self.seller_id = seller_id
        self.pid = pid
        self.num_items = num_items
        self.price = price
        self.status = status
        self.time_updated = time_updated
        self.time_purchased = time_purchased

    @staticmethod
    def get(order_id, seller_id, pid):
        rows = app.db.execute('''
SELECT order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated
FROM Purchases AS p
INNER JOIN Orders AS o
ON p.order_id = o.id
WHERE p.order_id = :id
WHERE p.seller_id = :seller_id
AND p.pid = :pid
''',
                              id=id,
                              seller_id=seller_id,
                              pid=pid)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated
FROM Purchases AS p
INNER JOIN Orders AS o
ON p.order_id = o.id
WHERE o.uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    def add_purchase(order_id, seller_id, pid, num_items, price, status, time_purchased):
        try:
            rows = app.db.execute('''
            INSERT INTO Purchases(order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated)
            VALUES (:order_id, :seller_id, :pid, :num_items, :price, :status, :time_purchased, :time_updated)
            ''',
            order_id=order_id,
            seller_id=seller_id,
            pid=pid,
            num_items=num_items,
            price=price,
            status=status,
            time_purchased=time_purchased,
            time_updated=time_purchased
            )
            return User.get(order_id, seller_id, pid)
        except Exception as e:
            print(str(e))
            return None
