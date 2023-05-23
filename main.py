import math

## calculate initial values
# reserves
xr = 100000000
yr = 100000000
k = xr * yr

# in-hand amounts
x0 = 10000
y0 = 0

# swap from x to y
delta_x = -xr + math.sqrt(xr * xr - xr * (xr * y0 - yr * x0) / (xr + y0))
delta_y = yr - k / (xr + delta_x)

print("delta_x = " + str(delta_x))
print(math.fabs((xr + delta_x) * (yr - delta_y) - k) < 1)
print(math.fabs((xr + delta_x) / (yr - delta_y) - (x0 - delta_x) / (y0 + delta_y)) < 1)

## calculate approximations
k = (xr * yr) * (xr * xr + yr * yr)

# derivatives
def dfdx(x, y):   # df/dx = 3x^2*y + y^3
    return 3 * x * x * y + y * y * y

def dfdy(x, y):   # df/dy = x^3 + 3xy^2
    return x * x * x + 3 * x * y * y

def f(x, y):
    return x * y * y * y + x * x * x * y

# loop
x = xr - delta_x
y = yr

for i in range(256):
    y_temp = y
    y += (k - x * y) / dfdy(x, y)
    if math.fabs(y - y_temp) < 1:
        print(i)
        break
print("x_start = " + str(x))
print("y_start = " + str(y))

# for i in range(51200):
#     x += (k - x * y) / dfdx(x, y)
#     y += (k - x * y) / dfdy(x, y)
#     print(x)
#     print(y)
#     print(math.fabs((xr + x) * (yr - y) - k) < 1)