import numpy as np
import regex as re
import os

class InvalidEquation(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def zeroify(arr1: list, arr2: list, index: int):
    product = np.dot(-arr2[index],arr1)
    return np.add(product, arr2)

def oneify(arr1: list, index:int):
    divisor = float(arr1[index])
    return (arr1 / divisor) if divisor else arr1

def main():
    running =  True
    print("Hello! This little tool will help you solve a linear algebra question using Gauss-Jordan Elimination.")
    while running:

        equations = []
        coefficients = []

        # ask the user for equations
        try:
            for n in range(3):
                eq = input(f"Enter equation #{n+1}: ").replace(" ","")
                equations.append(eq)
                coeff = [int(i) for i in re.findall("(\d+|-\d+)", eq)]
                if len(coeff) != 4:
                    raise InvalidEquation("At least one of your equation is invalid! Terminating program NOW")
                coefficients.append(coeff)
        except InvalidEquation as e:
            print(e.message)
            os.system("pause")
            exit(1)

        matrix = np.array(coefficients, dtype=float)
        print("Initial matrix:")
        print(matrix)

        iteration = 1
        # iteration 1 - 6
        for i in range(len(matrix)):
            matrix[i] = oneify(matrix[i], i)
            print(f"Iteration #{iteration}: \n{matrix}\n")
            iteration += 1

            for j in range(i+1, len(matrix)):
                matrix[j] = zeroify(matrix[i], matrix[j], i)
                print(f"Iteration #{iteration}: \n{matrix}\n")
                iteration += 1

        # iteration 7 - 9
        for i in range(len(matrix) - 1, 0, -1):
            for j in range(i-1, -1, -1):
                matrix[j] = zeroify(matrix[i], matrix[j], i)
                print(f"Iteration #{iteration}: \n{matrix}\n")
                iteration += 1

        resp = input("Terminate program? (\"y\" if yes)> ")
        if resp == "y":
            running = False

if __name__ == "__main__":
    main()