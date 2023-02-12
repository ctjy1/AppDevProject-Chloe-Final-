class feedback:

    def __init__(self, Feed, First_Name, Last_Name, Email, Phone_Number, Feedback):
        self.__Feed = Feed
        self.__First_Name = First_Name
        self.__Last_Name = Last_Name
        self.__Email = Email
        self.__Phone_Number = Phone_Number
        self.__Feedback = Feedback

    def get_Feed(self):
        return self.__Feed

    def get_First_Name(self):
        return self.__First_Name

    def get_Last_Name(self):
        return self.__Last_Name

    def get_Email(self):
        return self.__Email

    def get_Phone_Number(self):
        return self.__Phone_Number

    def get_Feedback(self):
        return self.__Feedback

    def set_Feed(self, Feed):
        self.__Feed = Feed

    def set_First_Name(self, First_Name):
        self.__First_Name = First_Name

    def set_Last_Name(self, Last_Name):
        self.__Last_Name = Last_Name

    def set_Email(self, Email):
        self.__Email = Email

    def set_Phone_Number(self, Phone_Number):
        self.__Phone_Number = Phone_Number

    def set_Feedback(self, Feedback):
        self.__Feedback = Feedback
