class NotANumber(Exception):  # המחלקה צריכה לרשת ממחלקת Exception
    """Custom exception input needs  a number"""

    def __init__(self, message="input a number"):
        self.message = message
        super().__init__(self.message)  # שליחת ההודעה למחלקת האב


class NotAString(Exception):
    """Custom exception input needs  a string"""

    def __init__(self, massage="input a string"):
        self.massage = massage
        super().__init__(self.massage)


class NotInRage(Exception):
    """Custom exception input needs be in the rage"""

    def __init__(self, massage="input a num in range"):
        self.massage = massage
        super().__init__(self.massage)
