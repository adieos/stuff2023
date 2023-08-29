import numpy as np
import regex as re

class InvalidEquation(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

print("Hello! This little tool will help you solve a linear algebra question using Gauss-Jordan Elimination.")

equations = []
coefficients = []

# ask the user for equations
try:
    for n in range(3):
        eq = input(f"Enter equation #{n+1}: ").replace(" ","")
        equations.append(eq)
        coeff = [int(i) for i in re.findall("(\d+|-\d+)", eq)]
        if len(coeff) != 4:
            raise InvalidEquation("At least one of your equation is invalid!")
        coefficients.append(coeff)
except InvalidEquation as e:
    print(e.message)

    
print(equations)
print(coefficients)