import numpy as np
from scipy.optimize import fsolve

wx = 9
wy = 6

def test(wx, wy):
    phi = (1 + np.sqrt(5)) / 2
    f = lambda b: 6 * b ** 3 \
        + (7 * wx + 2 * wy) * b ** 2 \
        + (wx * ((3 - phi)*wy + 2*wx)) * b \
        + (1 - phi) * wx ** 2 * wy

    b = fsolve(f, 1)[0]
    bottom = b + b ** 2 / (wx + b)
    return b, bottom

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        import timeit
        n = 1000
        print("Timing...")
        t = timeit.timeit('test(wx, wy)', setup="from __main__ import test, wx, wy", number=n)
        print("Time: {!r} for {!r} iterations, avg {!r}".format(t, n, t / n))
    else:
        b, bottom = test(wx, wy)

        print(
            "Print dimensions: {wx} x {wy}\n"
            "Resulting border: {b:.15}\n"
            "Resulting bottom border: {bottom:.15}"
            .format(wx=wx, wy=wy, b=b, bottom=bottom)
        )
