from abc import ABC, abstractmethod, abstractproperty


class BaseBuilder(ABC):

    @abstractproperty
    def browser(self):
        pass

    @abstractmethod
    def add_general_settings(self):
        pass

    @abstractmethod
    def add_docker_settings(self):
        pass

    @abstractmethod
    def add_headless_settings(self):
        pass
