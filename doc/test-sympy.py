from sympy import root as _root, symbols, collect, solve

wx = 9
wy = 6


def test(wx_value, wy_value):
    rphi = (1 + _root(5, 2)) / 2
    wx, wy, b, phi, bottom = symbols('wx,wy,b,phi, bottom')

    f = 6 * b ** 3 \
        + (7 * wx + 2 * wy) * b ** 2 \
        + (wx * ((3 - phi)*wy + 2*wx)) * b \
        + (1 - phi) * wx ** 2 * wy

    bottom = b + b ** 2 / (wx + b)

    # Collecting seems to help speed things up
    f_col = collect(f.subs({phi: rphi, wx: wx_value, wy: wy_value}), b)
    roots = solve(f_col, b)

    # We should have 2 imaginary numbers and one real..
    roots = [root for root in roots if not root.as_real_imag()[1]]
    if len(roots) < 1:
        raise Exception("Error, could not find solution for borders")
    elif len(roots) > 1:
        raise Exception("Error, multiple possible solutions for borders")

    b_value = roots[0].evalf(n=15)
    bottom_value = bottom.evalf(subs={b: b_value, wx: wx_value}, n=15)

    return b_value, bottom_value

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        import timeit
        n = 10
        print("Timing...")
        t = timeit.timeit('test(wx, wy)', setup="from __main__ import test, wx, wy", number=n)
        print("Time: {!r} for {!r} iterations, avg {!r}".format(t, n, t / n))
    else:
        b, bottom = test(wx, wy)

        print(
            "Print dimensions: {wx} x {wy}\n"
            "Resulting border: {b!s}\n"
            "Resulting bottom border: {bottom!s}"
            .format(wx=wx, wy=wy, b=b, bottom=bottom)
        )
