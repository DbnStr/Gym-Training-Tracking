from database.model import Model

class StrengthExercise(Model):

    name = None

    def __init__(self, id, start_datetime, finish_datetime,
                 training_id, strength_exercise_type_id, trainer_id):
        super().__init__()
        self.id = id
        self.start_datetime = start_datetime
        self.finish_datetime = finish_datetime
        self.training_id = training_id
        self.strength_exercise_type_id = strength_exercise_type_id
        self.trainer_id = trainer_id