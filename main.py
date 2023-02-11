import tkmacosx
import tkinter as tk


class Calculator:
    def __init__(self):
        """Initializing variables for the calculator"""
        self.solution_area = "0"
        self.prev_solution_area = ""
        self.prev_solution_label = None
        self.solution_label = None
        self.squared_formula = ""
        self.interface()

    def interface(self):
        """Creating a GUI interface for the calculator"""

        # Label for showing the solution area
        self.solution_label = tk.Label(win, text=self.solution_area,
                                       bg='#292c32', anchor='se',
                                       width=18, font=("Trebuchet MS", 39),
                                       )
        self.solution_label.place(x=0, y=90)

        # Label for showing the previous formula
        self.prev_solution_label = tk.Label(win, text=self.prev_solution_area,
                                            bg='#292c32', anchor='se',
                                            width=29, font=("Trebuchet MS", 23),
                                            )
        self.prev_solution_label.place(x=0, y=20)

        main_buttons = [
            "C", "<", ">", "(", ")",
            "1", "2", "3", "%", "X^2",
            "4", "5", "6", "*", "/",
            "7", "8", "9", "+", "-",
            "log()", "0", ".", "DEL", "="
        ]
        position_mb_x = 5
        position_mb_y = 180

        # Creating calculator buttons
        for btn in main_buttons:
            comm = lambda e=btn: self.logicalc(e)
            tkmacosx.Button(win, text=btn, bg='#30343a',
                            activebackground='#292c32',
                            font=("Times New Roman", 18), fg='white',
                            activeforeground='white',
                            command=comm,
                            ).place(x=position_mb_x, y=position_mb_y, width=70, height=79)

            position_mb_x += 80
            if position_mb_x > 400:
                position_mb_x = 5
                position_mb_y += 83.5

    def logicalc(self, action):
        """Logic of button actions"""
        overload_words = ["0", "Error", "True", "False"]
        block_words = ["DEL",
                       "=", "*", "/",
                       ">", "<", "%"]

        # Clear the solution area
        if action == "C":
            self.solution_area = "0"

        # Prohibit the use of "." in repetition and overload_words(exception 0)
        elif action == ".":
            if self.solution_area[-1] != "." and not self.solution_area in overload_words:
                self.solution_area += action
            elif self.solution_area == "0":
                self.solution_area += action

        # Writing a quadratic equation at the beginning and in the middle of the formula
        elif action == "X^2":
            if self.solution_area in overload_words:
                self.solution_area = f"( )²"
            else:
                self.solution_area = self.solution_area + f"( )²"

        # Writing a formula inside a quadratic equation
        elif self.solution_area[-1] == "²" and action != "=":
            self.solution_area = self.solution_area.replace(" ", "")

            # Exit condition for the quadratic equation
            if action != ")":
                self.solution_area = self.solution_area[:(len(self.solution_area)-2)] + ''.join(action) + \
                                     self.solution_area[(len(self.solution_area)-2):]
                self.squared_formula += action
            else:
                self.solution_area += " "

        # Prohibit adding characters in certain situations
        elif self.solution_area in overload_words:
            if not action in block_words and action != "X^2":
                self.solution_area = action

        # Delete the last character
        elif action == "DEL":
            self.solution_area = self.solution_area[0:-1]

        # Calculating the formula in the area
        elif action == "=":
            saved_formula = self.solution_area
            # Warning of a user error
            try:
                # Checking for and calculating a quadratic equation
                if "²" in self.solution_area:
                    solution_squared = str(eval(self.squared_formula) ** 2)
                    self.solution_area = self.solution_area.replace(f"({self.squared_formula})²",
                                                                    f"{solution_squared}")
                    self.squared_formula = ""
                self.solution_area = str(eval(self.solution_area))
            except (SyntaxError, ZeroDivisionError, NameError, TypeError):
                self.solution_area = "Error"
            # Writing down the whole equation with the answer
            self.prev_solution_label.configure(text=f"{saved_formula} = {self.solution_area}")

        # Adding characters to the area
        else:
            if " " in self.solution_area:
                self.solution_area = self.solution_area.replace(" ", action)
            else:
                self.solution_area += action
        self.update()

    def update(self):
        """Updating the solution area during actions"""
        self.solution_label.configure(text=self.solution_area)


if __name__ == "__main__":
    """Creating a window and running the program"""
    win = tk.Tk()
    win_w, win_h = 400, 600
    win.title("Calculator")
    win.geometry(f"{win_w}x{win_h}+0+10")
    logo = tk.PhotoImage(file='img/l_cal.png')
    win.iconphoto(False, logo)
    win.config(bg='#292c32')
    win.resizable(False, False)
    tk.Label(win, bg='#30343a',
             padx=200, pady=210).place(x=0, y=160)
    app = Calculator()
    win.mainloop()
