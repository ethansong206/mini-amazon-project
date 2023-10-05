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
        SELECT uid, I.seller_id, I.pid, num_items, in_cart, time_added, price
        FROM SavedItems S
        INNER JOIN Inventory as I
        ON I.seller_id = S.seller_id AND I.pid = I.pid
        WHERE uid = :uid
        AND in_cart
        ORDER BY time_added DESC
        ''',
        uid=uid)
        return rows if rows else []

    @staticmethod
    def get_all_wishlist_by_uid(uid):
        rows = app.db.execute('''
        SELECT uid, I.seller_id, I.pid, num_items, in_cart, time_added, price
        FROM SavedItems S
        INNER JOIN Inventory as I
        ON I.seller_id = S.seller_id AND I.pid = I.pid
        WHERE uid = :uid
        AND NOT in_cart
        ORDER BY time_added DESC
        ''',
        uid=uid)
        return rows if rows else []
    
    @staticmethod
    def add_item(uid, pid, num_items, in_cart, time_added):
        try:
            seller_id = app.db.execute('''
            SELECT seller_id
            FROM Products
            WHERE pid=:pid
            ''', pid=pid)[0][0]

            rows = app.db.execute('''
            INSERT INTO SavedItems(uid, seller_id, pid, num_items, in_cart, time_added)
            VALUES (:uid, :seller_id, :pid, :num_items, :in_cart, :time_added)
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

    @staticmethod
    def to_cart(uid, pid, time_added):
        try:
            seller_id = app.db.execute('''
            SELECT seller_id
            FROM Products
            WHERE pid=:pid
            ''', pid=pid)[0][0]

            rows = app.db.execute('''
            UPDATE SavedItems
            SET in_cart = True, time_added=:time_added
            WHERE uid=:uid
            AND pid=:pid
            AND seller_id=:seller_id
            ''',
            uid=uid,
            seller_id=seller_id,
            pid=pid,
            time_added=time_added
            )
            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def to_wishlist(uid, pid, time_added):
        try:
            seller_id = app.db.execute('''
            SELECT seller_id
            FROM Products
            WHERE pid=:pid
            ''', pid=pid)[0][0]

            rows = app.db.execute('''
            UPDATE SavedItems
            SET in_cart = False, time_added=:time_added
            WHERE uid=:uid
            AND pid=:pid
            AND seller_id=:seller_id
            ''',
            uid=uid,
            seller_id=seller_id,
            pid=pid,
            time_added=time_added
            )
            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(str(e))
            return None