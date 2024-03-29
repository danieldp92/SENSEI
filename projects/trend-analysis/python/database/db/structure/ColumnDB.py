class ColumnDB:
    def __init__(self, name, type, pk=False, not_null=False, auto_increment=False):
        self.name = name
        self.type = type
        self.pk = pk
        self.not_null = not_null
        self._auto_increment = auto_increment

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def pk(self):
        return self._pk

    @pk.setter
    def pk(self, value):
        self._pk = value

    @property
    def not_null(self):
        return self._not_null

    @not_null.setter
    def not_null(self, value):
        self._not_null = value

    @property
    def auto_increment(self):
        return self._auto_increment

    @auto_increment.setter
    def auto_increment(self, value):
        self._auto_increment = value