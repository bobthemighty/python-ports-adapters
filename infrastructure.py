""" This module contains infrastructural concerns

    In practice, a UnitOfWork is likely to be a thin wrapper over a SqlAlchemy
    session, and a UnitOfWorkManager to wrap over sessionmaker.

    A repository is a simple class which calls a session to perform db
    operations, where the session is provided in its constructor.

    The message bus implementation here is somewhat lacking because I can't
    decide what I think about IOC and DI. Pragmatically I think this would
    use inject to create a new handler. """


class UnitOfWorkManager:
    """Gives access to a unit of work

        This class is required only to implement Start which returns a
        UnitOfWork.

        Implementors must ensure that there is only a single unit of work
        for a given request context, eg. a web request or command pipeline

    """

    def start(self):
        raise NotImplementedError("start")


class UnitOfWork:
    """Represents a single logical set of operations against a data-store

        This class is a context manager and represents a db transaction. Kinda.

        If the commit method is not called before the context ends, the
        transaction must be rolled back.

        If the rollback method is called at any time, the tx immediately rolls
        back.

        If an exception occurs, this class ensures that the tx is rolled back
        automatically.

        Repositories are exposed as properties on a unit of work.

        A UnitOfWork must guarantee that database reads and writes occur
        within the same transactional scope"""

    def __enter__(self):
        raise NotImplementedError("enter")

    def __exit__(self, type, value, traceback):
        raise NotImplementedError("exit")

    def commit(self):
        raise NotImplementedError("commit")

    def rollback(self):
        raise NotImplementedError("rollback")

class Repository:
    """A Repository abstracts the notion of a data store.

        The basic repository pattern has three methods, Add, Get, and Delete
    """

    def __init__(self, uow_man):
        self.uow = uow_man

    def add(self, entity):
        """ Insert a new entity into the data store"""
        raise NotImplementedError("add")

    def delete(self, id):
        """Remove a persistent entity from the datastore"""
        raise NotImplementedError("delete")

    def get(self, id):
        """Fetch an entity from the datastore by its identifier.

            Changes to the entity will be tracked, and automatically saved
            back to the database when the UnitOfWork is committed"""
        raise NotImplementedError("get")


class MessageBus:
    """ Implements a simple message dispatcher interface

        This class is reponsible for creating a handler for a given command
        and executing the handler.

        Dependency injection and context management should also happen here """
    def __init__(self):
        self._handlers = {}

    def register(self, cmd, handler):
        if(cmd not in self._handlers):
            self._handlers[cmd] = [handler]
        elif(handler not in self._handlers[cmd]):
            self._handlers[cmd].append(handler)

    """ Send a Command to a single handler. If a command is not registered to
        exactly ONE handler, this method should fail """
    def send(self, cmd):
        t = type(cmd)
        handlers = self._handlers[t]
        if( len(handlers) != 1):
            raise "Bollocks!"

        handler = handlers[0]()
        handler(cmd)

    """ Send an event to any interested handlers. There may be any number of
        registered event handlers. This method will not fail if no handler
        can be found """
    def publish(self, event):
        pass
