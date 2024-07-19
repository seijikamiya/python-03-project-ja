from abc import ABC, abstractmethod
from getyfin import GetYfin

class BaseDB(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def create_db():
        pass

    @abstractmethod
    def insert_data():
        pass

class WeatherDB(BaseDB):
    pass

class StockDB(BaseDB):
    pass


def sql_query():
    pass