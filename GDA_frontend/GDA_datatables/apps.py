from django.apps import AppConfig


class SingletonMetaclass(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        assert not (args or kwargs), 'Singleton should not accept arguments'
        if isinstance(cls._instance, cls):
            return cls._instance
        else:
            cls._instance = super(SingletonMetaclass, cls).__call__()
            return cls._instance


class FrontendTracker(metaclass=SingletonMetaclass):
    def __init__(self):
        self.parsing = False
        self.progress = 0
        self.parsingStarted = False
        self.spinner = False
        self.showError = False

    def __call__(self):
        return self


class GdaDatatablesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GDA_datatables'
