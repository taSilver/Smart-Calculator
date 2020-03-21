"""
Author: Tim Silvester
Date modified: 21/03/2020
"""


class Calculator:
    vars = {}

    def interpret_equation(self, input_str):
        """
        Break down string into array with valid symbols
        :param input_str: The mathematical expression to be interpreted
        :return: An array containing either numbers, variables, or operators, or None if invalid
        :raises SyntaxError: If the expression is mal-formed
        :raises ValueError: If a variable is assigned incorrectly
        """
        reduced_str = []
        for item in input_str.split():
            if self.is_num(item) or item.isalpha():
                # if number or variable
                if not reduced_str or not str(reduced_str[-1]).isalnum():
                    reduced_str.append(int(item) if self.is_num(item) else item)
                else:
                    raise SyntaxError
            elif all(c in ["+", "-"] for c in item):
                # if mathematical operator
                reduced_str = self.eval_sub_add(reduced_str, item)
            elif item == "=":
                # If assignment operator
                if len(reduced_str) > 1 or "=" in reduced_str:
                    # check if more than one equals
                    raise ValueError
                reduced_str.append(item)
            elif item[0].isalpha() or item[0] == "=":
                # partial alphabet character
                eq_loc = self.find_eq(item)
                if eq_loc is None:
                    if "=" in reduced_str:
                        raise ValueError
                    else:
                        raise SyntaxError
                reduced_str = reduced_str + self.interpret_equation(
                    ' '.join([item[:eq_loc], item[eq_loc], item[eq_loc + 1:]]))
            else:
                # Not a number or alphabet or operator
                raise SyntaxError

        if reduced_str and not (self.is_num(reduced_str[-1]) or reduced_str[-1].isalpha()):
            # check if well formed expression
            raise SyntaxError
        return reduced_str

    def find_eq(self, input_str):
        """
        Locations the positions of the first equal operator within the given string
        :param input_str: The string to find the operator within
        :return: None if no equals is found, or an integer representing the position in the string
        :raises SyntaxError: If the expression is mal-formed
        :raises ValueError: If a variable is assigned incorrectly
        """
        eq_loc = None
        for sub_item in input_str:
            if not (self.is_num(sub_item) or sub_item.isalpha()) and sub_item != "=":
                # not alphabet or operator
                if eq_loc is None:
                    raise SyntaxError
                else:
                    raise ValueError
            elif sub_item == "=":
                # check if first assignment operator
                if not eq_loc:
                    eq_loc = input_str.find("=")
                else:
                    raise ValueError
        return eq_loc

    def eval_sub_add(self, lst, op):
        """
        Evaluate a given chain of subtraction and addition operators
        :param lst: The list that previous operators reside in
        :param op: The operator to currently identify
        :return: The list of operators with the new addition or subtraction operator added in
        :raises SyntaxError: If given operator doesn't correctly follow a chain
        """
        if len(op) > 1:
            for sub_item in op:
                if lst and not self.is_num(lst[-1]):
                    if sub_item + lst[-1] in ["++", "--"]:
                        lst[-1] = "+"
                    elif sub_item + lst[-1] in ["-+", "+-"]:
                        lst[-1] = "-"
                    else:
                        raise SyntaxError
                else:
                    lst.append(sub_item)
        else:
            if op != "=" or (len(lst) == 1 and lst[0].isalpha()):
                lst.append(op)
        return lst

    def is_num(self, num):
        """
        Utility function to check if given number is an integer
        :param num: The string to check if is a number
        :return: boolean true or false for if the string can be converted to a number
        """
        try:
            int(num)
            return True
        except ValueError:
            return False

    def retrieve_var(self, var):
        """
        Utility function to attempt to retrieve var from dictionary
        :param var: The string var to retrieve
        :return: Value of given var
        """
        return self.vars[var]

    def compute_list(self, lst):
        """
        Process mathematical expression in the form of a list
        :param lst: The mathematical expression
        :return: The result of the mathematical expression
        """
        # operations dictionary
        check_op = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
        }

        if lst:
            if len(lst) == 1:
                # if single item expression
                if type(lst[0]) == str:
                    var = self.retrieve_var(lst[0])
                    return var
                else:
                    return lst[0]

            res = ""
            while len(lst) > 2:
                if lst[1] == "=":
                    self.vars[lst[0]] = self.compute_list(lst[2:])
                    break
                val_1 = lst[0] if type(lst[0]) == int else self.retrieve_var(lst[0])
                val_2 = lst[2] if type(lst[2]) == int else self.retrieve_var(lst[2])

                res = check_op[lst[1]](val_1, val_2)
                lst = [res] + lst[3:]
            return res

    def calculate(self, input_str):
        """
        Main calculator function to calculate string
        :param input_str: The mathematical string to parse
        :return: None
        """
        try:
            reduced_str = self.interpret_equation(input_str)
            res = self.compute_list(reduced_str)
        except SyntaxError:
            print("Invalid expression")
        except ValueError:
            print("Invalid assignment")
        except KeyError:
            print("Unknown variable")
        else:
            print(res)


class Commands:
    def __init__(self):
        """
        Initialize the state of the calculator and map commands to functions
        """
        self.state = True
        self.command_map = {
            "/exit": self.exit_calc,
            "/help": self.help
        }

    def exit_calc(self):
        """
        Exit on next loop
        :return: Print string to console
        """
        self.state = False
        print("Bye!")

    def help(self):
        """
        Help command
        :return: Print information regarding calculator
        """
        print("The program calculates the sum, subtraction, multiplication, and division of numbers."
              "Variables can be stored and accessed later if required."
              "Bracketed expressions are supported.")

    def parse(self, command):
        """
        Parse the given command
        :param command: String representing the given command
        :return: Prints either unknown command or information relevant to given command
        """
        try:
            self.command_map[command]()
        except KeyError:
            print("Unknown command")
    

calc = Calculator()
command_interpreter = Commands()
while command_interpreter.state:
    input_str = input()
    if input_str:
        if input_str[0] == "/":
            command_interpreter.parse(input_str)
        else:
            calc.calculate(input_str)
