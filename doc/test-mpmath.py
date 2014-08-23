# import sympy.mpmath as mpmath
from mpmath import mp

mp.dps = 15
wx = mp.mpf('9')
wy = mp.mpf('6')


def test(wx, wy):
    phi = (1 + mp.sqrt(5)) / 2
    coeffs = [
        6,
        7 * wx + 2 * wy,
        wx * ((3 - phi)*wy + 2*wx),
        (1 - phi) * mp.power(wx, 2) * wy
    ]

    roots = mp.polyroots(coeffs, 15)
    roots = [root for root in roots if mp.im(root) == mp.mpf(0)]

    if len(roots) < 1:
        raise Exception("Error, could not find solution for borders")
    elif len(roots) > 1:
        raise Exception("Error, multiple possible solutions for borders")

    b = roots[0]
    bottom = b + mp.power(b, 2) / (wx + b)

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
            "Print dimensions: {wx!s} x {wy!s}\n"
            "Resulting border: {b!s}\n"
            "Resulting bottom border: {bottom!s}"
            .format(wx=wx, wy=wy, b=b, bottom=bottom)
        )
