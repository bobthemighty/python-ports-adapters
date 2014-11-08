from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products.infrastructure import UnitOfWork, Repository, UnitOfWorkManager


class SqlAlchemyUnitOfWorkManager(UnitOfWorkManager):

    _engine = create_engine('postgresql://bob:test@localhost/')

    def start(self):
        SqlAlchemyUnitOfWork(sessionmaker(bind=self.engine))


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session
        self.committed = False
        self._products = SqlAlchemyRepository(session)

    def __enter__(self):
        self.session.begin()

    def __exit__(self, value, type, traceback):
        if(self.committed is False):
            self.session.rollback()
        self.session.close()

    def rollback(self):
        self.session.rollback()
        self.session.close()
        self.committed = True

    def commit(self):
        self.session.flush()
        self.session.commit()
        self.session.close()
        self.session.committed = True

    @property
    def products(self):
        return self._products


class SqlAlchemyRepository(Repository):

    def __init__(self, session, cls):
        self._session = session
        self._cls = cls

    def add(self, entity):
        self._session.add(entity)

    def delete(self, entity):
        self._session.delete(entity)

    def get(self, id):
        self._session.query(self._cls).get(id)
