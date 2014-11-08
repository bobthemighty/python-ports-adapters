from products.test.infrastructure import FakeUnitOfWorkManager
from products.handlers import CreateProductCommand, CreateProductCommandHandler

class When_creating_a_product:
    """ Now that we have a repository pattern and command handlers
        it becomes trivial to write unit tests that check that
        we perform the correct actions against our domain.

        These tests should all operate against cmd handlers and verify that
        a) We create and commit a transaction
        b) We have persisted any state changes that we make
        c) We have raised any domain events on a message bus for further
            processing """

    def given(self):
        self._uow = FakeUnitOfWorkManager()
        self._handler = CreateProductCommandHandler(self._uow)

    def when_we_raise_a_create_product_command(self):
        self._handler(CreateProductCommand("foo"))

    def it_should_add_the_product_to_the_repository(self):
        assert any(p.name == "foo" for p in self._uow.products)

    def it_should_raise_product_created(self):
        pass

    def it_should_have_committed_the_unit_of_work(self):
        pass
