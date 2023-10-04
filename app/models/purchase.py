from flask import current_app as app


class Purchase:
    def __init__(self, order_id, seller_id, pid, num_items, price, time_updated):
        self.order_id = order_id
        self.seller_id = seller_id
        self.pid = pid
        self.num_items = num_items
        self.price = price
        self.time_updated = time_updated

    @staticmethod
    def get(order_id, seller_id, pid):
        rows = app.db.execute('''
SELECT order_id, seller_id, pid, num_items, price, time_updated
FROM Purchases
WHERE order_id = :order_id
AND seller_id = :seller_id
AND pid = :pid
''',
                              order_id = order_id,
                              seller_id = seller_id,
                              pid = pid)
        return Purchase(*(rows[0])) if rows else None

# this function is not needed for now
#     @staticmethod
#     def get_all_by_uid_since(uid, since):
#         rows = app.db.execute('''
# SELECT uid, pid, time_purchased
# FROM Purchases
# WHERE uid = :uid
# AND time_purchased >= :since
# ORDER BY time_purchased DESC
# ''',
#                               uid=uid,
#                               since=since)
#         return [Purchase(*row) for row in rows]
