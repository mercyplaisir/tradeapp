"""
got some useful math formula
"""


class Tool:
    """
    necessary tools to accomplish some task
    """

    @staticmethod
    def percent_calculator(number: float, percentage: float) -> float:
        """
        return z = z + z*x/100
        ex: 100 + 2% =102
        """
        z = number + ((number * percentage) / 100)
        return z

    @staticmethod
    def percent_change(original_number: float, new_number: float) -> int:
        """
        percent variation between two numbers
        ex: 100 and 98 -> -2%
        """
        z = ((new_number - original_number) / original_number) * 100
        return z
