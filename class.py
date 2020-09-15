import datetime

class ShowDate:
    def __init__(self):
        fecha = datetime.datetime.now()
        print(fecha)

fecha = ShowDate()