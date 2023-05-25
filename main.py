import math

# reserves
print("Params input:")
xr = 1472667531251509966538 # WETH
yr = 647408399605644450831 # WstETH

# in-hand amounts
x_in = 100 * 10 ** 18
y_in = 0
print("xr = " + str(xr / 10 ** 18) + ", yr = " + str(yr / 10 ** 18) + ", x_in = " + str(x_in / 10 ** 18) + ", y_in = " + str(y_in / 10 ** 18))

## use 'xy=k'
print("Find swap solution with 'xy=k':")
k = xr * yr

# swap from x to y
alpha = (y_in + yr) / (x_in + xr)
beta = alpha
x0 = (k / beta) ** (1 / 2)
y0 = k / x0

## the comparison between delta_x and delta_y show a big slippage
print("x = " + str(x0 / 10 ** 18))
print("y = " + str(y0 / 10 ** 18))
assert(math.fabs((x_in - (x0 - xr)) / (y_in + (yr - y0)) - (x0 / y0)) < 10 ** -6)

## use 'xy^3+yx^3=k'
k = (xr * yr) * (xr * xr + yr * yr)

# derivatives
def dfdx(x, y):   # df/dx=3x^2*y+y^3
    return 3 * x * x * y + y * y * y

def dfdy(x, y):   # df/dy=x^3+3xy^2
    return x * x * x + 3 * x * y * y

# calculate k
def f(x, y):
    return x * y * y * y + x * x * x * y

def get_y(x, y):
    for i in range(256):
        y_temp = y
        y += (k - f(x, y)) / dfdy(x, y)
        if math.fabs(y - y_temp) < 1:
            break
    return y

y0 = get_y(x0, yr)
print("But the real 'y' for this `x` should be: " + str(y0 / 10 ** 18))

# find the best point on 'xy^3+yx^3=k'
print("Find swap solution with 'xy^3+yx^3=k':")
alpha = (y_in + yr) / (x_in + xr)
beta = alpha + alpha ** 3
x1 = (k / beta) ** (1 / 4)
y1 = get_y(x1, yr)

print("x = " + str(x1 / 10 ** 18))
print("y = " + str(y1 / 10 ** 18))
assert(math.fabs((x_in - (x1 - xr)) / (y_in + (yr - y1)) - (x1 / y1)) < 10 ** -6)

# compare between with fee and without fee
real_delta_y = 28.004410421688815616
print("Compare between with fee and without fee:")
print("delta_x = " + str((x1 - xr) / 10 ** 18))
print("delta_y = " + str((yr - y1) / 10 ** 18))
print("But the real 'delta_y' we can get: " + str(real_delta_y)) 