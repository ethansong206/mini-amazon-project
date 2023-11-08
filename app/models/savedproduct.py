from flask import current_app as app

from .inventory import Inventory
from .order import Order
from .purchase import Purchase

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
    def submit_order(uid, time_purchased):
        try:

            # CHECK IF ENOUGH INVENTORY BEFORE SUBMITTING
            # ALSO CHECK IF ENOUGH BALANCE

            # record uid, status, time_purchased, timestamp, total_price
            # insert into Order and return id
            # insert each product into Purchases with new order id
            # remove the products from saveditems and from inventory
            items = app.db.execute('''
            SELECT *
            FROM SavedItems
            WHERE uid=:uid
            AND in_cart
            ''',
            uid=uid
            )

            order = app.db.execute('''
            INSERT INTO Orders(uid, status, timestamp)
            VALUES(:uid, :status, :timestamp)
            RETURNING id
            ''',
            uid=uid,
            status='Pending',
            timestamp=time_purchased)

            orderid = order[0][0]

            for item in items:
                # get item price
                inventory_item = app.db.execute('''
                SELECT price, quantity
                FROM Inventory
                WHERE pid=:pid
                AND seller_id=:seller_id
                ''',
                pid=item.pid,
                seller_id=item.seller_id)

                if len(inventory_item) == 0:
                    return

                print(inventory_item)

                priceperitem = inventory_item[0][0]
                qty = inventory_item[0][1]

                if qty < item.num_items:
                    return

                # check if enough balance
                

                # delete item from inventory
                deleted = app.db.execute('''
                UPDATE Inventory
                SET quantity = quantity - :qty
                WHERE pid = :pid
                AND seller_id = :seller_id
                ''',
                pid=item.pid,
                seller_id=item.seller_id,
                qty=item.num_items)

                # delete item from saveditems

                deleted = app.db.execute('''
                DELETE FROM SavedItems
                WHERE pid=:pid
                AND seller_id=:seller_id
                AND uid=:uid
                ''',
                uid=uid,
                pid=item.pid,
                seller_id=item.seller_id,
                qty=item.num_items)

                # add item to purchases

                purchase = app.db.execute('''
                INSERT INTO Purchases(order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated)
                VALUES(:order_id, :seller_id, :pid, :num_items, :price, :status, :time_purchased, :time_updated)
                ''',
                order_id=orderid,
                seller_id=item.seller_id,
                pid=item.pid,
                num_items=item.num_items,
                price=priceperitem)
                print(item.uid)

            

            return orderid
            
        except Exception as e:
            print(e)
            print('error')
            return None

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
            print('exception')
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
        # this will have a check to see if the quantity is less than inventory
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

    @staticmethod
    def remove_item(uid, seller_id, pid):
        try:
            rows = app.db.execute('''
            DELETE FROM SavedItems
            WHERE uid=:uid
            AND seller_id=:seller_id
            AND pid=:pid
            ''',
            uid=uid,
            seller_id=seller_id,
            pid=pid
            )
            return
        except Exception as e:
            print(e)
            return None

