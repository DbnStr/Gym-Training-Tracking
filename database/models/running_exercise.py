from database.model import Model

class RunningExercise(Model):

    name = None

    def __init__(self, id, start_datetime, finish_datetime,
                 distance, time, average_speed, average_pulse,
                 min_pulse, max_pulse, running_exercise_type_id,
                 training_id, trainer_id):
        super().__init__()
        self.id = id
        self.start_datetime = start_datetime
        self.finish_datetime = finish_datetime
        self.distance = distance
        self.time = time
        self.average_speed = average_speed
        self.average_pulse = average_pulse
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.running_exercise_type_id = running_exercise_type_id
        self.training_id = training_id
        self.trainer_id = trainer_id