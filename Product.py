class Product:
    count_id = 1

    def __init__(self, file, product_name, product_price, product_status, product_amount, product_description):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__file = file
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_status = product_status
        self.__product_amount = product_amount
        self.__product_description = product_description

    def get_product_id(self):
        return self.__product_id

    def get_file(self):
        return self.__file

    def get_product_name(self):
        return self.__product_name

    def get_product_price(self):
        return self.__product_price

    def get_product_status(self):
        return self.__product_status

    def get_product_amount(self):
        return self.__product_amount

    def get_product_description(self):
        return self.__product_description

    # mutator methods
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_file(self, file):
        self.__file = file

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_price(self, product_price):
        self.__product_price = product_price

    def set_product_status(self, product_status):
        self.__product_status = product_status

    def set_product_amount(self, product_amount):
        self.__product_amount = product_amount

    def set_product_description(self, product_description):
        self.__product_description = product_description
