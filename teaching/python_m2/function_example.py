#%%
from dataclasses import dataclass
import numpy as np

@dataclass
class Polynomial:
    coefficients: list # [1, 2, 3] - > 1 + 2*x + 3*x^2

    def function(self):
        return lambda x : np.sum([self. coefficients[i]*x**i for i in range(len(self.coefficients))])
    
vba_code = "Polynomial([1,2,3])" # this should come from the text file that vba writes

my_polynomial = eval(vba_code)
# %%
my_function = my_polynomial.function()
# %%
my_function(7)
# %%
# 1 + 2*7 + 3*7^2