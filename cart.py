import json
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    
    # Changed to check 'if cart_details is None' -> 'if cart_details is None' check.
    if cart_details is None:
        return []

    items = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        
        try:
            # Replaced eval() with json.loads() to securely parse JSON data.
            evaluated_contents = json.loads(contents)  
        except json.JSONDecodeError:
            continue  # Skip cart if contents cannot be parsed.
        
        # Using list comprehension to fetch products based on the parsed contents
        items.extend([products.get_product(content) for content in evaluated_contents])
    
    return items


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
