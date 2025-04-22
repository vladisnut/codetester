from settings import TEST_TYPE
from testing.general import testing
from testing.test_type import TestType


def main():
    """
    Тесты должны быть разделены хотя бы одной пустой строкой.
    Первые N строк теста – входные параметры тестируемой функции.
    (N + 1)-я строка содержит ожидаемое возвращаемое значение
    тестируемой функции (необязательно).
    """
    with open('tests.txt', 'r', encoding='utf-8') as f:
        testing(getattr(TestType, TEST_TYPE.upper()), f.read())


if __name__ == '__main__':
    main()
