from time_allocator_core.client import Model

# python src/time_allocator_core/tests.py


class TestModel(Model):
    value: float


def test_debug():
    TestModel(value=1000000.23).print_debug()


if __name__ == "__main__":
    test_debug()
