import tkinter as tk
import unittest
from main import Calculator


class Test_Calculator_Logicalc(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_logicalc_C(self):
        self.calculator.logicalc("CE")
        self.assertEqual(self.calculator.solution_area, "0")

    def test_logicalc_0(self):
        self.calculator.solution_area = "0"
        self.calculator.logicalc(".")
        self.assertEqual(self.calculator.solution_area, "0.")

        self.calculator.solution_area = "0"
        self.calculator.logicalc("3")
        self.assertEqual(self.calculator.solution_area, "3")

        self.calculator.solution_area = "0"
        self.calculator.logicalc(">")
        self.assertEqual(self.calculator.solution_area, "0")

    def test_logicalc_bracket(self):
        self.calculator.solution_area = "0"
        self.calculator.logicalc("(")
        self.assertEqual(self.calculator.solution_area, "( )")

        self.calculator.solution_area = "9+"
        self.calculator.logicalc("(")
        self.assertEqual(self.calculator.solution_area, "9+( )")

        self.calculator.solution_area = "9+(3-1)"
        self.calculator.logicalc(")")
        self.assertEqual(self.calculator.solution_area, "9+(3-1) ")

        self.calculator.solution_area = "0"
        self.calculator.logicalc("X^2")
        self.assertEqual(self.calculator.solution_area, "( )²")

    def test_logicalc_power(self):
        self.calculator.solution_area = "9+"
        self.calculator.logicalc("X^2")
        self.assertEqual(self.calculator.solution_area, "9+( )²")

        self.calculator.solution_area = "( )²"
        self.calculator.logicalc("9")
        self.assertEqual(self.calculator.solution_area, "(9)²")

        self.calculator.solution_area = "9+(2-4)²"
        self.calculator.logicalc(")")
        self.assertEqual(self.calculator.solution_area, "9+(2-4)² ")

    def test_logicalc_percent(self):
        self.calculator.solution_area = "15-((200-50)+((200-50)*10/100))+40"
        self.calculator.logicalc("=")
        self.assertEqual(self.calculator.solution_area, "121.0")

    def test_logicalc_del(self):
        self.calculator.solution_area = "3-1"
        self.calculator.logicalc("DEL")
        self.assertEqual(self.calculator.solution_area, "3-")

        self.calculator.solution_area = "3-(3-1)"
        self.calculator.logicalc("DEL")
        self.assertEqual(self.calculator.solution_area, "3-(3-)")

        self.calculator.solution_area = "3-(3-1)²"
        self.calculator.logicalc("DEL")
        self.assertEqual(self.calculator.solution_area, "3-(3-)²")

        self.calculator.solution_area = "3-()"
        self.calculator.logicalc("DEL")
        self.assertEqual(self.calculator.solution_area, "3-")

        self.calculator.solution_area = "3-()²"
        self.calculator.logicalc("DEL")
        self.assertEqual(self.calculator.solution_area, "3-")

    def test_logicalc_error(self):
        self.calculator.solution_area = "2+()"
        self.calculator.logicalc("=")
        self.assertEqual(self.calculator.solution_area, "Error")
        self.assertTrue(isinstance(self.calculator.mistake_win, tk.Toplevel))

        error_label = self.calculator.mistake_win.children["!label"]
        label_text = error_label["text"]
        self.assertEqual(label_text[0: + label_text.find(":")], "TypeError")


if __name__ == '__main__':
    unittest.main()
