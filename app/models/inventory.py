from flask import current_app as app

class Inventory:
    def __init__(self, seller_id, pid, price, quantity):
        self.self = self
        self.seller_id = seller_id
        self.pid = pid
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get(pid, seller_id):
        rows = app.db.execute('''
        SELECT seller_id, pid, price, quantity
        FROM Inventory
        WHERE pid = :pid
        AND seller_id = :seller_id
        ''',
                              pid=pid,
                              seller_id=seller_id)
        return Inventory(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all_from_seller(seller_id):
        rows = app.db.execute('''
        SELECT seller_id, pid, price, quantity, name
        FROM Inventory
        JOIN Products ON Products.id = pid
        WHERE seller_id = :seller_id;
        ''',
                              seller_id=seller_id)
        return rows if rows else []

    @staticmethod
    def update_inventory_price(pid, seller_id, new_price):
        # this will have a check to see if the quantity is less than inventory
        try:
            rows = app.db.execute('''
            UPDATE Inventory
            SET price = :new_price
            WHERE seller_id=:seller_id
            AND pid=:pid
            ''',
            seller_id=seller_id,
            new_price=new_price,
            pid=pid
            )
            return Inventory.get(pid, seller_id)
        except Exception as e:
            print(e)
            print('excpetion')
            return None

    @staticmethod
    def update_inventory_qty(pid, seller_id, new_qty):
        # this will have a check to see if the quantity is less than inventory
        try:
            rows = app.db.execute('''
            UPDATE Inventory
            SET quantity = :new_qty
            WHERE seller_id=:seller_id
            AND pid=:pid
            ''',
            seller_id=seller_id,
            new_qty=new_qty,
            pid=pid
            )
            return Inventory.get(pid, seller_id)
        except Exception as e:
            print(e)
            print('excpetion')
            return None
