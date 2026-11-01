import numpy as np
from scipy import stats

def loss_rate(times_weeks, log_values, level):
    n = len(times_weeks)
    if n < 3:
        raise ValueError("too few points")
    if n != len(log_values):
        raise ValueError("Different lengths between the weeks and log-values")
    fit = stats.linregress(times_weeks,log_values)
    t_crit = stats.t.ppf(1 - (1 - level) / 2, n - 2)    # n = len(times_weeks)
    uncertainty = (fit.stderr)
    loss = -(fit.slope)
    low = (loss - t_crit * uncertainty)
    high = (loss + t_crit * uncertainty)
   
    return loss, low, high

def verdict(low, high, bound=0.1):
    if high < bound:
      return 'supported'
    elif low > bound:
      return 'rejected'
    else:
      return 'inconclusive' # if low or high is NaN, both are false, function guranteed returns inconclusive
    
    
