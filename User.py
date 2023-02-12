# User class
class User:
    # count_id = 0

    def __init__(self, count_id, firstname, lastname, username, email, phone, password, password_confirm):
        # User.count_id += 1
        self.__user_id = count_id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__email = email
        self.__phone = phone
        self.__password = password
        self.__password_confirm = password_confirm
        self.__points = 0

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_password(self):
        return self.__password

    def get_password_confirm(self):
        return self.__password_confirm

    def get_points(self):
        return self.__points


    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def set_lastname(self, lastname):
        self.__lastname = lastname

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone

    def set_password(self, password):
        self.__password = password

    def set_password_confirm(self, password_confirm):
        self.__password_confirm = password_confirm

    def set_points(self, points):
        self.__points = points

    def update_points(self, points):
        self.__points = self.__points - points
