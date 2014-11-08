from products.infrastructure import Repository, UnitOfWorkManager


class FakeUnitOfWorkManager(UnitOfWorkManager):

    def __init__(self):
        self._products = FakeRepository()


    def start(self):
        return self

    @property
    def products(self):
        return self._products

    def __exit__(self, type, value, traceback):
        pass

    def __enter__(self):
        return self

    def commit(self):
        pass

class FakeRepository(Repository):

    def __init__(self):
        self.entities = []

    def add(self, entity):
        print("adding item to entities")
        self.entities.append(entity)

    def __iter__(self):
        return self.entities.__iter__()
