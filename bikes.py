class bikes:

    def __init__(self, Damage_ID, Bike_ID, date, damage, payment):
        self.__Damage_ID = Damage_ID
        self.__Bike_ID = Bike_ID
        self.__date = date
        self.__damage = damage
        self.__payment = payment

    def get_Damage_ID(self):
        return self.__Damage_ID

    def get_Bike_ID(self):
        return self.__Bike_ID

    def get_date(self):
        return self.__date

    def get_damage(self):
        return self.__damage

    def get_payment(self):
        return self.__payment

    def set_Damage_ID(self, Damage_ID):
        self.__Damage_ID = Damage_ID

    def set_Bike_ID(self, Bike_ID):
        self.__Bike_ID = Bike_ID

    def set_date(self, date):
        self.__date = date

    def set_damage(self, damage):
        self.__damage = damage

    def set_payment(self, payment):
        self.__payment = payment
