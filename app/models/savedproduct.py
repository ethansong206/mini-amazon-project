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
        SELECT uid, seller_id, pid, num_items, time_added
        FROM SavedItems
        WHERE uid = :uid
        AND seller_id = :seller_id
        AND pid = :pid
        ''',
        uid=uid,
        seller_id=seller_id,
        pid=pid
        )
        print('getting item')

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
        return rows if rows else []

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
        return rows if rows else []

    @staticmethod
    def add_to_cart(uid, seller_id, pid, num_items, time_added):
        try:
            rows = app.db.execute('''
            INSERT INTO SavedItems(uid, seller_id, pid, num_items, in_cart, time_added)
            VALUES(:uid, :sid, :pid, num_items, :in_cart, :time_added)
            ''',
            uid=uid,
            sid=seller_id,
            pid=pid,
            num_items=num_items,
            in_cart=True,
            time_added=time_added
            )
            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            return None

    def move_to_cart(uid, seller_id, pid, time_added):
        try:
            rows = app.db.execute('''
            UPDATE SavedItems
            SET in_cart=:in_cart, time_added=:time_added
            WHERE uid=:uid
            AND seller_id=:sid
            AND pid=:pid
            ''',
            uid=uid,
            sid=seller_id,
            pid=pid,
            in_cart=True,
            time_added=time_added
            )

            # app.db.commit()

            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(e)
            print('excpetion')
            return None

    def move_to_wishlist(uid, seller_id, pid, time_added):
        try:
            rows = app.db.execute('''
            UPDATE SavedItems
            SET in_cart=:in_cart, time_added=:time_added
            WHERE uid=:uid
            AND seller_id=:sid
            AND pid=:pid
            ''',
            uid=uid,
            sid=seller_id,
            pid=pid,
            in_cart=False,
            time_added=time_added
            )

            # app.db.commit()

            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(e)
            print('excpetion')
            return None

    @staticmethod
    def update_quantity(uid, seller_id, pid, num_items):
        try:
            rows = app.db.execute('''
            UPDATE SavedItems
            SET num_items = :num_items
            WHERE uid=:uid
            AND seller_id=:seller_id
            AND pid=:pid
            ''',
            uid=uid,
            seller_id=seller_id,
            pid=pid,
            num_items=num_items
            )
            return SavedItem.get(uid, seller_id, pid)
        except Exception as e:
            print(e)
            print('excpetion')
            return None