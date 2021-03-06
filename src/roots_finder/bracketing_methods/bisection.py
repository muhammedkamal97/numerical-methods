import timeit
import numpy
from src.roots_finder.equations_parser import *


class Bisection:

    def solve(self, equation, *args, max_iterations=50, epsilon=0.0001):
        # Parsing arguments
        if len(args) < 2:
            raise TypeError("Missing arguments")
        left = args[0]
        right = args[1]
        if len(args) > 2:
            max_iterations = args[2]
        if len(args) > 3:
            epsilon = args[3]

        number_of_iterations = 0
        start_time = timeit.default_timer()
        # Parsing string into a func using Sympy lib and throw exception if the function not valid
        try:
            expression = equation_to_expression(equation)
            x = get_symbol(expression)
            func = expression_to_lambda(x, expression)
        except ValueError:
            raise ValueError("Not a valid function")

        approximate_root = 0
        prev_approx = 0
        error = 100
        iterations = []  # Iteration array to store each iteration
        # Iterations
        while True:
            left_value, right_value = func(left), func(right)
            # Handling if this interval has odd roots between left and and right (At least one root)
            if left_value * right_value > 0:
                raise ValueError("Bisection can't find a root for this interval")
            approximate_root = (left + right) / 2
            approximate_root_value = func(approximate_root)

            iteration = numpy.array((left, right, approximate_root, error),
                                    dtype=[('xl', numpy.float), ('xu', numpy.float), ('xr', numpy.float),
                                           ('err', numpy.float)])
            error = abs((approximate_root - prev_approx) / approximate_root) * 100
            iterations.append(iteration)
            # Determine the next interval
            if approximate_root_value * left_value < 0:
                right = approximate_root
            elif approximate_root_value * left_value > 0:
                left = approximate_root
            else:
                break
            prev_approx = approximate_root
            number_of_iterations += 1
            if abs(right - left) < epsilon or number_of_iterations > max_iterations:
                break

        execution_time = timeit.default_timer() - start_time

        return number_of_iterations, execution_time, iterations, approximate_root, error, func
