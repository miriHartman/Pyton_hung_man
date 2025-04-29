import random


class User:

    # מחלקת משתמש

    def __init__(self, user_name, user_pass):  # יצירת בנאי
        self.user_name = user_name
        self.user_pass = user_pass
        self.num_play = 0
        self.set_words = {''}
        self.num_win = 0

    # @classmethod
    # def __init__(self, user_name, user_pass, num_play, set_words, num_win):  # יצירת בנאי
    #     super(self, user_name, user_pass)
    #     # self.user_name = user_name
    #     # self.user_pass = user_pass
    #     self.num_play = num_play
    #     self.set_words = set_words
    #     self.num_win = num_win

    def __str__(self):
        return "{"+f'"user_name":"{self.user_name}", "user_pass":"{self.user_pass}","num_play":"{self.num_play}","set_words":"{self.set_words}", "num_win":"{self.num_win}"'+"}"

