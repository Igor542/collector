class Transaction:
    def __init__(self, tx_id, time, user, value, comment):
        self.tx_id = tx_id
        self.time = time
        self.user = user
        self.value = value
        self.comment = comment

    def __str__(self):
        return f'tx:{{id:{self.tx_id}, user:{self.user}, value:{self.value}, comment:"{self.comment}"}}'

    def __repr__(self):
        print(str(self))
