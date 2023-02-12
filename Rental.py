# Rental Class
class Rental:

    def __init__(self, full_name, phone_no, email, date, time_in, time_out, bicycle, duration, count):
        self.__customer_id = count + 1
        self.__full_name = full_name
        self.__phone_no = phone_no
        self.__email = email
        self.__date = date
        self.__time_in = time_in
        self.__time_out = time_out
        self.__bicycle = bicycle
        self.__duration = duration

    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_full_name(self):
        return self.__full_name

    def get_phone_no(self):
        return self.__phone_no

    def get_email(self):
        return self.__email

    def get_date(self):
        return self.__date

    def get_time_in(self):
        return self.__time_in

    def get_time_out(self):
        return self.__time_out

    def get_bicycle(self):
        return self.__bicycle

    def get_duration(self):
        return self.__duration

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_email(self, email):
        self.__email = email

    def set_date(self, date):
        self.__date = date

    def set_time_in(self, time_in):
        self.__time_in = time_in

    def set_time_out(self, time_out):
        self.__time_out = time_out

    def set_bicycle(self, bicycle):
        self.__bicycle = bicycle

    def set_duration(self, duration):
        self.__duration = duration
