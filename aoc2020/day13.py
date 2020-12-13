import math

file1 = open('day_13_input.txt', 'r')
lines = file1.read().splitlines()

earliest = int(lines[0])
buses = lines[1].split(',')
running_buses = []
bus_res = []
for i, b in enumerate(buses):
    if b.isnumeric():
        running_buses.append(int(b))
        bus_res.append(-i)

min_time = earliest * 100000
min_bus = -1
for b in running_buses:
    time = math.ceil(earliest/b) * b
    if time < min_time:
        min_time = time
        min_bus = b

print((min_time-earliest) * min_bus)


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n%2 == 0:
        return False
    if n < 9:
        return True
    if n%3 == 0:
        return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        # print('\t',f)
        if n % f == 0:
            return False
        if n % (f+2) == 0:
            return False
        f += 6
    return True


def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quot = old_r // r
        old_r, r = r, old_r - quot * r
        old_s, s = s, old_s - quot * s
        old_t, t = t, old_t - quot * t

    return (old_s, old_t), old_r, (t, s)


def chinese_remainder_thm(mods, res):
    N = 1
    for m in mods:
        N *= m
    x = 0
    for i, ni in enumerate(mods):
        Ni = N//ni
        bezout, _, _ = extended_gcd(Ni, ni)
        x += res[i] * bezout[0] * Ni

    return x % N


print(chinese_remainder_thm(running_buses, bus_res))