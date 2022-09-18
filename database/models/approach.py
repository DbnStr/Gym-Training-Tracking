from database.model import Model

class Approach(Model):
    def __init__(self, id, start_datetime, finish_datetime, weight,
                 repetition, strength_exercise_id):
        super().__init__()
        self.id = id
        self.start_datetime = start_datetime
        self.finish_datetime = finish_datetime
        self.weight = weight
        self.repetition = repetition
        self.strength_exercise_id = strength_exercise_id
        self.duration = int(round((finish_datetime - start_datetime).total_seconds() / 60))