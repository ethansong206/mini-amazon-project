from flask import current_app as app

from .inventory import Inventory

class SavedItem:
    def __init__(self, uid, seller_id, pid, num_items, in_cart, time_added):
        self.uid = uid
        self.seller_id = seller_id
        self.pid = pid
        self.num_items = num_items
        self.in_cart = in_cart
        self.time_added = time_added

    @staticmethod
    def get(uid, seller_id, pid):
        rows = app.db.execute('''
        SELECT S.uid, S.seller_id, S.pid, S.num_items, S.in_cart, I.price, S.time_added
        FROM SavedItems as S
        INNER JOIN Inventory as I
        ON S.seller_id = I.seller_id
        AND S.pid = I.pid
        WHERE S.uid = :uid
        AND S.seller_id = :seller_id
        AND S.pid = :pid
        ''',
        uid=uid,
        seller_id=seller_id,
        pid=pid
        )
        return SavedItem(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_cart_by_uid(uid):
        rows = app.db.execute('''
        SELECT uid, seller_id, pid, num_items, time_added
        FROM SavedItems
        WHERE uid = :uid
        AND in_cart
        ORDER BY time_added DESC
        ''',
        uid=uid)
        return [SavedItem(*row) for row in rows]

    @staticmethod
    def get_all_wishlist_by_uid(uid):
        rows = app.db.execute('''
        SELECT uid, seller_id, pid, num_items, time_added
        FROM SavedItems
        WHERE uid = :uid
        AND NOT in_cart
        ORDER BY time_added DESC
        ''',
        uid=uid)
        return [SavedItem(*row) for row in rows]
    
    @staticmethod
    def add_item(uid, seller_id, pid, num_items, in_cart, time_added):
        try:
            rows = app.db.execute('''
            INSERT INTO SavedItems(uid, seller_id, pid, num_items, in_cart, time_added)
            VALUES (uid, seller_id, pid, num_items, in_cart, time_added)
            ''',
            uid=uid,
            seller_id=seller_id,
            pid=pid,
            num_items=num_items,
            in_cart=in_cart,
            time_added=time_added
            )
            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(str(e))
            return None