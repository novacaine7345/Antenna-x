import numpy as np
#import pandas as pan
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
import math
import csv

y_vals = []
x_vals = []
with open('antenna_dataset_Gs_full(4).csv', 'r') as file :
    csvreader = csv.reader(file)
    next(csvreader)    
    for line in csvreader:
        y_vals.append(float(line[16]))
        x_vals.append(float(line[1]))
        
    
step = 501
#x_vals = [0, 50, 100, 150, 200]
#x_vals = np.linspace(1, 500, step)
#y_vals = [0, 60, 100, 120, 80]
#print(x_vals)
#print(y_vals)
x_interp = float(input("Enter the Required Frequency : "))

def forward_difference_table(y):
    n = len(y)
    diff_table= np.zeros((n, n))
    diff_table[:, 0] = y
    
    for j in range (1, n):
        for i in range (n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j-1]
    return diff_table

def newton_forward_interpolation(x_val, y_val, x) : 
    n = len(x_val)
    h = x_val[1] - x_val[0] 
    diff_table = forward_difference_table(y_val)
    
    p = (x - x_val[0]) / h
    result = y_val[0]
    
    p_term = 1
    for i in range(1, n) : 
        p_term *= (p - (i - 1))
        result += (p_term * diff_table[0][i] ) / math.factorial(i)
    return result

xplot_min = 0
xvals_max = len(x_vals) 
xplot_max = int(x_vals[xvals_max-1])

poly = CubicSpline(x_vals, y_vals)
x = np.linspace(3, xplot_max)
y = poly(x)


#print(f'Interpolated value at x = {x_interp} is {newton_forward_interpolation(x_vals, y_vals, x)}')
#print('Print the polynomial : ', CubicSpline(x_vals, y_vals))
print(f'The S1,1 value at {x_interp} is (dB) = ', poly(x_interp))


plt.figure(figsize=(20, 12))
plt.plot(x_vals, y_vals,'r*',label='original Data', markersize=3)
plt.plot(x, y, 'b--', label='Scipy Polynomial')
plt.plot(x_interp, poly(x_interp), 'ko', label='Test point', markersize=6)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()

plt.show()
