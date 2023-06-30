from enum import Enum
from abc import ABC, abstractclassmethod

class Choices(Enum):
    """
    All types of Models that the user can choose
    """
    BLACK_SCHOLES = 'Black Scholes Model'
    MONTE_CARLO = 'Monte Carlo Simulation'
    BINOMIAL = 'Binomial Model'

class Option(Enum):
    """
    Types of Options
    """
    CALL = "Call Option"
    PUT = "Put Option"

class OptionModels(ABC):
    """
    ABSTRACTCLASS: The backbone of a option pricing model
    
    """

    def calc_price(self, o_type):
        """
        Calculates the price of an option

        Params:
        o_type: Call or Put
        """
        if o_type == Option.CALL.value:
            return self.calc_call_price()
        elif o_type == Option.PUT.value:
            return self.calc_put_price()
        else:
            return -1
        
    @abstractclassmethod
    def calc_call_price(self):
        pass

    @abstractclassmethod
    def calc_put_price(self):
        pass

    

