class SonarqubeBean:
    def __init__(self, timestamp, project_name, page, metrics):
        self._timestamp = timestamp
        self._project_name = project_name
        self._page = page
        self._metrics = metrics

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    @staticmethod
    def __prop__():
        return [key for key in SonarqubeBean.__dict__
                if not key.startswith("_") and "property object at" in str(SonarqubeBean.__dict__[key])]
