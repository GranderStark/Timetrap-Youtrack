class Application:
    instance = None

    def __getattr__(self, item, *args, **kwargs):
        return self.__dict__[item]

    def __setattr__(self, name, value):
        self.__dict__[name] = value


app = Application()
