import datetime
import pickle

class DateMessage:
    def __init__(self, message: str):
        self.date = datetime.datetime.now()
        self.message = message

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
