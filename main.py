import sys
import tkinter as tk
from tkinter import Button
import re

if sys.platform == 'darwin':
    from tkmacosx import Button


class Calculator:
    def __init__(self):
        """Initializing variables for the calculator"""
        self.mistake_win = None
        self.solution_area = "0"
        self.prev_solution_area = ""
        self.prev_solution_label = None
        self.solution_label = None
        self.squared_formula = ""
        self.create_interface()

    def create_interface(self):
        """Creating a GUI interface for the calculator"""

        # Solution label
        self.solution_label = tk.Label(text=self.solution_area,
                                       bg='#292c32', anchor='se',
                                       width=18, font=("Trebuchet MS", 39),
                                       )
        self.solution_label.place(x=0, y=90)

        # Previous solution label
        self.prev_solution_label = tk.Label(text=self.prev_solution_area,
                                            bg='#292c32', anchor='se',
                                            width=29, font=("Trebuchet MS", 23),
                                            )
        self.prev_solution_label.place(x=0, y=20)

        main_buttons = [
            "CE", "<", ">", "(", ")",
            "1", "2", "3", "%", "X^2",
            "4", "5", "6", "*", "/",
            "7", "8", "9", "+", "-",
            "", "0", ".", "DEL", "="
        ]
        position_mb_x = 5
        position_mb_y = 180

        for btn in main_buttons:
            self.create_button(btn, position_mb_x, position_mb_y)
            position_mb_x += 80
            if position_mb_x > 400:
                position_mb_x = 5
                position_mb_y += 83.5

    def create_button(self, btn_text, x, y):
        """Creating calculator buttons"""

        comm = lambda: self.logicalc(btn_text)
        Button(text=btn_text, bg='#30343a',
               activebackground='#292c32',
               font=("Times New Roman", 18), fg='white',
               activeforeground='white',
               command=comm,
               ).place(x=x, y=y, width=70, height=79)

    def logicalc(self, action):
        """Logic of button actions"""

        overload_words = {"0", "Error", "True", "False"}
        block_ops = {"DEL", "=", "*", "/", ">", "<", "%"}
        formula = self.solution_area

        # Clear the solution area
        if action == "CE":
            formula = ""

        # Write the equation in parentheses
        elif action == "(":
            if formula in overload_words:
                formula = f"( )"
            else:
                formula += f"( )"

        # Writing a quadratic equation
        elif action == "X^2":
            if formula in overload_words:
                formula = f"( )²"
            else:
                formula += f"( )²"

        # Writing a formula inside the equation in parentheses
        elif formula[-1] in [")", "²"] and action not in ["=", "DEL"]:
            formula = formula.replace(" ", "")

            # Exit condition for the equation
            if action != ")":
                if formula[-1] == ")":
                    formula = formula[:len(formula) - 1] + ''.join(
                        action) + formula[(len(formula) - 1):]
                elif formula[-1] == "²":
                    formula = formula[:len(formula) - 2] + ''.join(action) + \
                              formula[(len(formula) - 2):]
                    self.squared_formula += action
            else:
                formula += " "

        # Prohibit the use of "." in repetition and overload_words(exception 0)
        elif action == ".":
            if formula not in overload_words and formula[-1] != ".":
                formula += action
            elif formula == "0":
                formula += action

        # Prohibit adding characters in certain situations
        elif formula in overload_words:
            if action not in block_ops and action != "X^2":
                formula = action

        # Delete the last character
        elif action == "DEL":
            # Delete the last character in parentheses
            if formula[-1] == ")":
                if not formula[-2] == "(":
                    formula = formula[:len(formula) - 2] + ")"
                else:
                    formula = formula[:len(formula) - 2]
            elif formula[-1] == "²":
                if formula[-3] != "(":
                    formula = formula[:len(formula) - 3] + ")²"
                    self.squared_formula = self.squared_formula[0:-1]
                else:
                    formula = formula[:len(formula) - 3]
            else:
                formula = formula[0:-1]

        # Calculating the formula in the area
        elif action == "=":
            saved_formula = formula
            # Warning of a user error
            try:
                # Calculating a formula with percentages
                if "%" in formula:
                    for count_percent in range(formula.count("%")):

                        # Divide the formula into two parts and find the percentage
                        split_formula = re.split("%", formula, 1)  # = ["15-(200-50)+10", "+40"]
                        formula_before_percent = split_formula[0]  # = 15-(200-50)+10
                        formula_after_percent = split_formula[1]  # = +40
                        split_formula_before_percent = re.split(r"\D", formula_before_percent)  # = ["15", "", "200","50", "", "10"]
                        percent = split_formula_before_percent[-1]  # = 10

                        if len(split_formula_before_percent) > 1:
                            ops_before_percentage = formula_before_percent[:-(len(percent))][-1]  # = 15-(200-50)+ -> +

                            # Check for parentheses before the sign
                            if split_formula_before_percent[-2] == "":
                                before_last_bracketed_formula = formula_before_percent[
                                                                0: + formula_before_percent.rfind("(")]  # = 15-
                                after_last_bracketed_formula = formula_before_percent[
                                                               formula_before_percent.rfind("(") + 0:]  # = (200-50)+10

                                # Check round brackets or square brackets
                                round_squared = ")²" if split_formula_before_percent[-3] == "" else ")"  # = )
                                bracketed_formula = after_last_bracketed_formula[
                                                    0: + after_last_bracketed_formula.find(")")] + round_squared  # = (200-50)

                                formula = f"{before_last_bracketed_formula}" \
                                          f"({bracketed_formula}{ops_before_percentage}({bracketed_formula}*{percent}/100))" \
                                          f"{formula_after_percent}"  # = 15-((200-50)+((200-50)*10/100))+40
                            else:
                                # Finding a number from which we take a percentage
                                dependent_number = split_formula_before_percent[-2]
                                count_active_number = len(dependent_number + percent) + 1

                                formula_before_dependent_number = formula_before_percent[:-count_active_number]

                                formula = f"{formula_before_dependent_number}" \
                                          f"({dependent_number}{ops_before_percentage}({dependent_number}*{percent}/100))" \
                                          f"{formula_after_percent}"
                        else:
                            formula = f"({percent}/100){formula_after_percent}"
                        count_percent += 1

                # Checking for and calculating a quadratic equation
                if "²" in formula:
                    solution_squared = str(eval(self.squared_formula) ** 2)
                    formula = formula.replace(f"({self.squared_formula})²", f"{solution_squared}")
                    self.squared_formula = ""
                formula = str(eval(formula))
            except (SyntaxError, ZeroDivisionError, NameError, TypeError) as exception:
                error_message = f"{type(exception).__name__}: {exception.args[0]}"
                self.error_warning(error_message)
                formula = "Error"
            # Writing down the whole equation with the answer
            self.prev_solution_label.configure(text=f"{saved_formula} = {formula}")

        # Adding characters to the area
        else:
            if " " in formula:
                formula = formula.replace(" ", action)
            else:
                formula += action

        self.solution_area = formula
        self.update()

    def error_warning(self, message):
        """Create a new window for an error"""

        self.mistake_win = tk.Toplevel()
        self.mistake_win.geometry("390x75+5+55")
        self.mistake_win.title('Error message')
        self.mistake_win.config(bg='#292c32')
        tk.Label(self.mistake_win, text=f'{message}', bg='#FF6666',
                 font='Arial 15 bold', fg='white', height=2, width=40, wraplength=370
                 ).place(relx=0.5, rely=0.5, anchor="center")
        self.mistake_win.overrideredirect(True)
        self.mistake_win.after(3000, lambda: self.mistake_win.destroy())

    def update(self):
        """Updating the solution area during actions"""
        if self.solution_area == "":
            self.solution_area = "0"
        self.solution_label.configure(text=self.solution_area)


if __name__ == "__main__":
    """Creating a window and running the program"""
    win = tk.Tk()
    win_w, win_h = 400, 600
    win.title("Calculator")
    win.geometry(f"{win_w}x{win_h}+0+10")
    logo = tk.PhotoImage(file='img/calculator_icon.png')
    win.iconphoto(False, logo)
    win.config(bg='#292c32')
    win.resizable(False, False)
    tk.Label(win, bg='#30343a',
             padx=200, pady=210).place(x=0, y=160)
    app = Calculator()
    win.mainloop()
