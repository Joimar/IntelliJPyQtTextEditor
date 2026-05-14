

class ConfigManager:
    _instance = None
    def __new__(cls):
        # in case the instance does not exist
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # Initialization of default settings
            cls._instance.font_size = 12
            cls._instance.theme = "light"
            cls._instance.auto_save = False
        return cls._instance