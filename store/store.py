from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Store:
    def __init__(self, driver="sqlite://"):
        self.driver = create_engine(driver, future=True)

    def connect(self):
        self.session = Session(self.driver)
    def close(self):
        self.session.close()