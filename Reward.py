class Reward:

    def __init__(self, reward_id, reward_name, discount, points_required, reward_expiry, remarks):
        self.__reward_id = reward_id
        self.__name = reward_name
        self.__discount = discount
        self.__points_required = points_required
        self.__reward_expiry = reward_expiry
        self.__remarks = remarks

    # accessor methods

    def get_reward_id(self):
        return self.__reward_id

    def get_name(self):
        return self.__name

    def get_discount(self):
        return self.__discount

    def get_points_required(self):
        return self.__points_required

    def get_reward_expiry(self):
        return self.__reward_expiry

    def get_remarks(self):
        return self.__remarks

    # mutator methods

    def set_reward_id(self, reward_id):
        self.__reward_id = reward_id

    def set_name(self, reward_name):
        self.__name = reward_name

    def set_discount(self, discount):
        self.__discount = discount

    def set_points_required(self, points_required):
        self.__points_required = points_required

    def set_reward_expiry(self, reward_expiry):
        self.__reward_expiry = reward_expiry

    def set_remarks(self, remarks):
        self.__remarks = remarks
