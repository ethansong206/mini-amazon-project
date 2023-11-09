from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, balance, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, balance, address
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, balance, address
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def get_purchase_history(uid):
        rows = app.db.execute('''
SELECT order_id, seller_id, pid, num_items, price, status, time_purchased, time_updated, name
FROM Purchases
JOIN Products ON Products.id = Purchases.pid
WHERE order_id IN (
    SELECT id FROM Orders
    WHERE uid = :uid
)
ORDER BY time_updated DESC
''',
                              uid = uid)
        columns = ['order_id', 'seller_id', 'pid', 'num_items', 'price', 'status', 'time_purchased', 'time_updated', 'name']
        return rows if rows else []
    
    @staticmethod
    def update_firstname(id, new_firstname):
        try:
            app.db.execute("""
                UPDATE Users
                SET firstname = :new_firstname
                WHERE id = :id
            """, new_firstname=new_firstname, id=id)
            return
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_lastname(id, new_lastname):
        try:
            app.db.execute("""
                UPDATE Users
                SET lastname = :new_lastname
                WHERE id = :id
            """, new_lastname=new_lastname, id=id)
            return
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_address(id, new_address):
        try:
            app.db.execute("""
                UPDATE Users
                SET address = :new_address
                WHERE id = :id
            """, new_address=new_address, id=id)
            return
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_email(id, new_email):
        try:
            app.db.execute("""
                UPDATE Users
                SET email = :new_email
                WHERE id = :id
            """, new_email=new_email, id=id)
            return
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def update_balance(id, new_balance):
        try:
            app.db.execute("""
                UPDATE Users
                SET balance = :new_balance
                WHERE id = :id
            """, new_balance=new_balance, id=id)
            return
        except Exception as e:
            print(str(e))
            return None
