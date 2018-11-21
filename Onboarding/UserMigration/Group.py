import numpy as np

class Group(object):
    

    def __init__(self, id1, id2, name):
        self.id1 = id1
        self.id2 = id2
        self.name = name
        self.users = None

    def add_users(self, user_list):
        self.users = user_list

    def check_user(self, user_email):
        if (self.users is None):
            return False
        if (np.size(self.users) == 0):
            return False
        for i in np.arange(0, np.size(self.users)):
            if (user_email == self.users[i]):
                return True
        return False

    def __str__(self):
        return str(self.name) + "is " + str(self.id1) + " : " + str(self.id2)