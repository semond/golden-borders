# -*- coding: utf-8 -*-
"""
Compute nice borders for a print.

The borders are computed so the area of the mat equals the
area of the window times "Golden Ratio".

They are also computed so that the top, left and right borders
are the same, and the bottom border is bigger to compensate for
the optical illusion that the print "sinks" into the mat.

This also allows to use "Golden Ratio"^2 for bigger borders, and
any multiplicator to that.

It's also possible to compute the print size from a desired mat
size.

:copyright: © 2014, Serge Émond
:license: not specified

"""

from __future__ import absolute_import, print_function, \
        unicode_literals, division

import click
import re
from mpmath import mp
mp.dps = 15

# Precision to use when printing dimensions
PRECS = {
    'mm': 1,
    'cm': 2,
    'dm': 3,
    'm': 4,
    'in': 2,
    'ft': 4,
}
POSSIBLE_UNITS = ['mm', 'cm', 'dm', 'm', 'in', 'ft']
_punits = '(?P<u>' + '|'.join(POSSIBLE_UNITS) + ')?$'
_dim_re = re.compile(r'(?P<v>[0-9.-]+)' + _punits)
_dim_pair_re = re.compile(r'(?P<w>[0-9.]+)(?P<sep>x|X|,|:|-)(?P<h>[0-9.]+)' + _punits)

# The Golden Ratio
PHI = (1 + mp.sqrt(5)) / 2


def compute_border_sizes(dims, phi, mat=False):
    """Compute optimal border sizes for a mat window mesuring dims[0] x dims[1].

    Returns a tuple (top_left_right_border, bottom_border).

    The computed top, left and right borders have the same value.

    The computed bottom border is bigger to compensate for the
    optical illusion of the picture "sinking" in the frame.

    The values are computed so that the mat's surface is the window's
    surface times `phi`.

    Passing `mat=True` causes the computation to be reversed: the borders
    are computed from a mat size.
    """
    x, y = dims[0], dims[1]
    if mat:
        # dims are mat's dims
        coeffs = [
            -2 * phi,
            5 * x * phi + 2 * y * phi,
            -2 * x * x * phi - 3 * x * y * phi + x * y,
            x * x * y * (phi - 1),
        ]
        A = lambda b: b * b / (x - b)
    else:
        # dims are window's dims
        coeffs = [
            6,
            7 * x + 2 * y,
            x * ((3 - phi)*y + 2*x),
            (1 - phi) * mp.power(x, 2) * y
        ]
        A = lambda b: b * b / (x + b)

    roots = mp.polyroots(coeffs, 50)
    roots = [root for root in roots if mp.im(root) == mp.mpf(0)]

    # If multiple solutions, keep the one with smalest borders first
    roots.sort()
    sols = [
        # (root, root + mp.power(root, 2) / (x + root))
        (root, root + A(root))
        for root in roots
    ]

    # Shouldn't happen
    if len(roots) < 1:
        raise Exception("Error, could not find solution for borders")
    elif len(roots) > 1:
        click.echo("*Warning: multiple solutions. Keeping smallest border.", err=True)

    return sols[0]


def to_mm(dim, units=None, inverse=False):
    dim = mp.mpf(dim)
    if units == 'cm':
        mult = mp.mpf(10)
    elif units == 'dm':
        mult = mp.mpf(100)
    elif units == 'm':
        mult = mp.mpf(1000)
    elif units == 'in':
        mult = mp.mpf('25.4')
    elif units == 'ft':
        mult = mp.mpf('304.8')
    else:
        mult = mp.mpf('1')

    if inverse:
        # convert *from* mm
        return dim / mult
    return dim * mult


def parse_dim(dstr, default_units=None):
    """Parse a string dimension to mm"""
    m = _dim_re.match(dstr)
    if not m:
        click.echo("ERROR: Can't parse dimension {!r}".format(dstr), err=True)
        return None

    units = m.group('u')
    dim = m.group('v')

    if not units:
        units = default_units

    return to_mm(dim, units)


def parse_dim_pair(dstr, default_units=None):
    """Parse a string representing a pair of dimensions, to mm"""
    m = _dim_pair_re.match(dstr)
    if not m:
        click.echo("ERROR: Can't parse dimension pair {!r}".format(dstr), err=True)
        return None

    units = m.group('u')
    width = m.group('w')
    height = m.group('h')

    if not units:
        units = default_units

    return to_mm(width, units), to_mm(height, units)


def dim_str(dim, units):
    """Format a dimension to a given unit"""
    dim = to_mm(dim, units, True)
    prefix = ''
    if units == 'ft':
        if dim >= mp.mpf(1):
            prefix = str(int(mp.floor(dim))) + "'"
        units = 'in'
        dim = mp.frac(dim) * 12
    dim = prefix + ("{:." + str(PRECS[units]) + "f}").format(float(mp.nstr(dim)))
    if units == 'in':
        return dim + '"'

    return dim + ' ' + units


def dim_pair_str(dims, units):
    return '{} x {}'.format(dim_str(dims[0], units), dim_str(dims[1], units))


@click.command()
@click.argument('print-dims')
@click.option('--overlap', default='0', help="Overlap of mat's window over the print")
@click.option('--units', default='mm', help="Default unit, also used for output")
@click.option('--paper', default='0x0', help="Dims of the paper of the print, assumed to be centered")
@click.option('--phi', default='phi', help="PHI to use: phi, phi-square")
@click.option('--mat/--print', default=False, help='PRINT_DIMS are mat/print size, default print')
def main(print_dims, overlap, units, paper, phi, mat):
    """Compute something.

    Dimensions can be passed using a simple [<width><sep><height><units>]
    structure, where:

        <sep> can be 'x', ',' or ':'

        <width> and <height> are numbers, possibly floats (like 1.8)

        <units> is optional and may be mm, cm, dm, in, ft

    Example: 9x6in

    A single dimension can be written as [<dim><unit>]. If <unit> is
    unspecified, it is assumed to be the same as the print size.
    """
    default_units = units if units in POSSIBLE_UNITS else 'mm'
    if units and units not in POSSIBLE_UNITS:
        click.echo(
            "ERROR: Unknown units, {!r}, defaulting to mm"
            .format(units), err=True)

    overlap = parse_dim(overlap, default_units=default_units)
    print_dims = parse_dim_pair(print_dims, default_units=default_units)
    paper_dims = parse_dim_pair(paper, default_units=default_units)
    phi_value = mp.power(PHI, 2) if phi == 'phi-square' else PHI

    if mat:
        # print is mat, compute window and print sizes
        mat_dims = print_dims

        b, b_bottom = compute_border_sizes(mat_dims, phi_value, mat=True)

        window_dims = (
            mat_dims[0] - 2 * b,
            mat_dims[1] - b - b_bottom,
        )

        print_dims = [dim + overlap * 2 for dim in window_dims]

    else:
        # print is print, compute mat and window sizes
        window_dims = [dim - overlap * 2 for dim in print_dims]

        b, b_bottom = compute_border_sizes(window_dims, phi_value, mat=False)

        mat_dims = (
            window_dims[0] + 2 * b,
            window_dims[1] + b + b_bottom
        )

    if paper_dims[0] < print_dims[0] or paper_dims[1] < print_dims[1]:
        paper_dims = [dim for dim in print_dims]

    paper_borders = (
        (paper_dims[0] - print_dims[0]) / 2,
        (paper_dims[1] - print_dims[1]) / 2,
    )

    paper_shift = (
        b - overlap - paper_borders[0],
        b - overlap - paper_borders[1],
    )

    print('== Parameters ============================================')
    print(
        "Print size        {print}\n"
        "Paper size        {paper}\n"
        "Window overlap    {overlap}\n"
        "Mat window size * {win}"
        .format(
            print=dim_pair_str(print_dims, units),
            paper=dim_pair_str(paper_dims, units),
            overlap=dim_str(overlap, units),
            win=dim_pair_str(window_dims, units),
        ))

    print('\n== Mat Information ========================================')
    print(
        "Mat size        * {mat}\n"
        "Window position\n"
        "  Top           * {top}\n"
        "  Bottom        * {bottom}\n"
        "  Left / Right  * {lr}"
        .format(
            mat=dim_pair_str(mat_dims, units),
            top=dim_str(b, units),
            bottom=dim_str(b_bottom, units),
            lr=dim_str(b, units),
        ))

    print('\n== Paper position from sides of mat =======================')
    print(
        "  Top           * {top}\n"
        "  Bottom        * {bottom}\n"
        "  Left          * {left}\n"
        "  Right         * {right}"
        .format(
            top=dim_str(paper_shift[1], units),
            bottom=dim_str(mat_dims[1] - paper_dims[1] - paper_shift[1], units),
            left=dim_str(paper_shift[0], units),
            right=dim_str(mat_dims[0] - paper_dims[0] - paper_shift[0], units),
        ))


if __name__ == '__main__':
    main()
