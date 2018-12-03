from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class SqlLitePart:
    engine = None
    session = None
    address = None
    config = None
    __configuration_name__ = 'db'

    def __init__(self, **kwargs):
        for n, v in kwargs.items():
            setattr(self, n, v)
        self.initialise_part()

    def initialise_part(self):

        self.address = self.config.get('url')
        self.create_session()

    def create_session(self):
        self.engine = create_engine(self.address)
        _Session = scoped_session(sessionmaker())

        self.session = _Session(bind=self.engine)

    def destroy_session(self):
        if self.session:
            self.session.close()
