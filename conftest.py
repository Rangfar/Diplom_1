import pytest
from burger import Burger

@pytest.fixture
def burger():
    burger = Burger()
    return burger