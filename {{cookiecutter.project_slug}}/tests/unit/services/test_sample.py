from tests.unit.services import FakeRepository


def test_service_sample():
    repo = FakeRepository()
    assert type(repo) == FakeRepository
    # result = list_samples(repo)
    # assert type(result) == dict
