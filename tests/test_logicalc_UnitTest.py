from unittest import TestCase, main
from main import Calculator


class LogiacalcTest(TestCase):
    def test_plus(self):
        self.assertEqual(str(eval("6*9.0-4")), "50.0")


if __name__ == '__main__':
    main()
