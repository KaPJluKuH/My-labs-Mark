from DbContext import DbContext


class SingleContext:

    def __init__(self, path):
        self.context = DbContext(path)
        self.path = path

    def get_instance(self) -> DbContext:
        try:
            self.context.connection.commit()
            return self.context
        except:
            self.context = DbContext(self.path)
            return self.context

