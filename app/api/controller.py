
from datetime import date

class Collection():
    ''' Constructor Initialization '''
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def calculateAge(self, year, month, day): 
        today = date.today() 
        age = today.year - year - ((today.month, today.day) < (month, day)) 
    
        return age 