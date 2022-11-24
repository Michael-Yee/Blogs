class Config(object):
    DEBUG = False
    MESSAGE = "World!"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MESSAGE = "Mike!"
