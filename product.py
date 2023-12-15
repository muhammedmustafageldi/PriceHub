class Product:

    def __init__(self, name, store, img_url, price, product_url):
        self.name = name
        self.store = store
        self.img_url = img_url
        self.price = price
        self.product_url = product_url

    def __str__(self):
        return f'Product name: {self.name}\nStore: {self.store}\nImage url: {self.img_url}\nPrice: {self.price}\nProduct url: {self.product_url}'
