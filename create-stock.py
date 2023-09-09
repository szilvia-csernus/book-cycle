import json
import random

with open('backup-book-2.json', 'r') as json_file:
    books = json.load(json_file)

array_of_stock = []

for book in books:
    fields_new = {
        "book": book["pk"],
        "condition": "new",
        "price": round((random.uniform(15, 55.5)), 1),
        "quantity": random.randint(0, 10)
    }
    array_of_stock.append(
        {
            "model": "inventory.stock",
            "fields": fields_new
        }
    )
    fields_good = {
        "book": book["pk"],
        "condition": "good",
        "price": round((fields_new["price"]*0.6), 1),
        "quantity": random.randint(0, 5)
    }
    array_of_stock.append(
        {
            "model": "inventory.stock",
            "fields": fields_good
        }
    )
    fields_fair = {
        "book": book["pk"],
        "condition": "fair",
        "price": round((fields_new["price"]*0.4), 1),
        "quantity": random.randint(0, 5)
    }
    array_of_stock.append(
        {
            "model": "inventory.stock",
            "fields": fields_fair
        }
    )

with open('stock.json', "w") as json_file:
    json.dump(array_of_stock, json_file)
