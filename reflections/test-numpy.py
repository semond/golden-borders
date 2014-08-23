import numpy as np

wx = 9
wy = 6

def test(wx, wy):
    phi = (1 + np.sqrt(5)) / 2

    roots = np.roots([
        6,
        7 * wx + 2 * wy,
        wx * ((3 - phi)*wy + 2*wx),
        (1 - phi) * np.square(wx) * wy
    ])

    reals = [root for root in roots if not root.imag]
    if len(reals) < 1:
        raise Exception("Error, could not find solution for borders")
    elif len(reals) > 1:
        raise Exception("Error, multiple possible solutions for borders")

    b = reals[0].real
    bottom = b + np.square(b) / (wx + b)

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
