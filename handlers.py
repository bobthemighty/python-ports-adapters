from products.model import Product
from products.infrastructure import UnitOfWorkManager, MessageBus

class CreateProductCommandHandler:
    """ Command handlers all follow the same pattern:

            Begin a transaction
            Obtain current state
            Mutate state
            Commit the transaction
            Raise any domain events

        Part of me wants to sack these off and replace them with
        functions since it's trivial to inject named args to a function
        in python """

    def __init__(self, uow=UnitOfWorkManager(), bus=MessageBus()):
        self._uow = uow
        self._bus = bus

    def __call__(self, cmd):
        p = Product(cmd.name)
        with self._uow.start() as tx:
            tx.products.add(p)
            tx.commit()
        self._bus.publish(ProductUpdatedEvent())


class UpdateProductNameCommandHandler:

    def __init__(self, uow=UnitOfWorkManager()):
        self._uow = uow

    def __call__(self, cmd):
        with self._uow.start() as tx:
            product = tx.products.get(cmd.id)
            product.name = cmd.name
            tx.commit()


class CreateProductCommand:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

class ProductUpdatedEvent:
    pass
