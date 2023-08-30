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
    print(divisor)
    return (arr1 / divisor) if divisor else arr1

if __name__ == "__main__":
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
        os.system("pause")
        exit(1)

    matrix = np.array(coefficients, dtype=float)
    print("Initial matrix:")
    print(matrix)

    # 1st iteration
    matrix[0] = oneify(matrix[0], 0)
    print(f"First iteration: \n{matrix}\n")

    # 2nd iteration
    matrix[1] = zeroify(matrix[0], matrix[1], 0)
    print(f"Second iteration: \n{matrix}\n")

    # 3rd iteration
    matrix[2] = zeroify(matrix[0], matrix[2], 0)
    print(f"Third iteration: \n{matrix}\n")

    # 4th iteration
    matrix[1] = oneify(matrix[1], 1)
    print(f"Fourth iteration: \n{matrix}\n")

    # 5th iteration
    matrix[2] = zeroify(matrix[1], matrix[2], 1)
    print(f"Fifth iteration: \n{matrix}\n")

    # 6th iteration:
    matrix[2] = oneify(matrix[2], 2)
    print(f"Sixth iteration: \n{matrix}")




    os.system("pause")