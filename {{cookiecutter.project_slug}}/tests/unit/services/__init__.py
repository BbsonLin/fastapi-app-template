from app.repository import AbstractRepository


class FakeRepository(AbstractRepository):

    def __init__(self):
        self._datas = list()

    def add(self, data):
        self._datas.append(data)

    def add_and_commit(self, data):
        self._datas.append(data)

    def get(self):
        return self._datas[0]

    def list(self):
        return self._datas

    def list_all(self):
        return self._datas

    def list_by_date_range(self, **kwargs):
        return self._datas


class FakeSession():
    committed = False

    def commit(self):
        self.committed = True
