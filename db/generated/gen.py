from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_inventory_items = 1000
num_orders = 1000
categories = ["Appliances", "Automotive Parts & Accessories", "Beauty & Personal Care", "Books & Media", "Clothing", "Shoes & Jewelry", "Electronics", "Grocery & Gourmet Food", "Health", "Household & Baby Care", "Home & Kitchen", "Sports & Outdoors", "Toys"]

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = 0
            writer.writerow([uid, email, password, firstname, lastname, None, balance])
        print(f'{num_users} generated')
    return

def gen_random_seller_id():
    seller_id = fake.random_int(min=0, max=num_users-1)
    # Generated seller ids will be odd
    if seller_id % 2 == 0:
        seller_id = seller_id + 1
    return seller_id

def gen_products(num_products):
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            creator_id = gen_random_seller_id()
            name = fake.sentence(nb_words=4)[:-1]
            category = fake.random_element(elements=categories)
            description = fake.sentence(nb_words=20)[:-1]
            writer.writerow([pid, creator_id, name, category, description, ""])
        print(f'{num_products} generated')
    return

def gen_orders(num_orders):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for id in range(num_orders):
            uid = fake.random_int(min=0, max=num_users-1)
            status = fake.random_element(elements=["Pending", "On Hold", "Fulfilled"])
            timestamp = fake.date_time()
            writer.writerow([id, uid, status, timestamp])
        return


def gen_purchases(num_purchases, available_pids):
    # with open('Purchases.csv', 'w') as f:
    #     writer = get_csv_writer(f)
    #     print('Purchases...', end=' ', flush=True)
    #     for id in range(num_purchases):
    #         if id % 100 == 0:
    #             print(f'{id}', end=' ', flush=True)
    #         uid = fake.random_int(min=0, max=num_users-1)
    #         pid = fake.random_element(elements=available_pids)
    #         time_purchased = fake.date_time()
    #         writer.writerow([id, uid, pid, time_purchased])
    #     print(f'{num_purchases} generated')
    return

def gen_categories():
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...')
        for category in categories:
            writer.writerow([category])
    print(f'{len(categories)} generated')

def gen_sellers():
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...')
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            # All odd number uids will be sellers
            if uid % 2 == 1:
                writer.writerow([uid])
    print(f'{int(num_users / 2)} generated')

def gen_inventories():
    already_generated = {}
    with open('Inventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...')
        for id in range(num_inventory_items):
            seller_id = gen_random_seller_id()
            pid = fake.random_int(min=0, max=num_products-1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=0, max=1000)
            # Prevent duplicate seller_id and pid combinations from being generated
            if seller_id not in already_generated.keys():
                already_generated[seller_id] = []
            if pid not in already_generated[seller_id]:
                already_generated[seller_id].append(pid)
                writer.writerow([seller_id, pid, price, quantity])
        print(f'{num_inventory_items} generated')
    return

# gen_users(num_users)
gen_products(num_products)
# gen_purchases(num_purchases, available_pids)
gen_categories()
gen_sellers()
gen_inventories()
gen_orders(num_orders)
