from database.model import Model

class Training(Model):
    def __init__(self, id, start_datetime, finish_datetime, customer_id):
        super().__init__()
        self.id = id
        self.start_datetime = start_datetime
        self.finish_datetime = finish_datetime
        self.customer_id = customer_id