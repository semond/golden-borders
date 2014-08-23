from mpmath import mp

mp.dps = 5

wx = mp.mpf('9'); wy = mp.mpf('6')
phi = (1 + mp.sqrt(5)) / 2
phi = mp.power(phi, 2)
coeffs = [
    6,
    7 * wx + 2 * wy,
    wx * ((3 - phi)*wy + 2*wx),
    (1 - phi) * mp.power(wx, 2) * wy
]

roots = mp.polyroots(coeffs, 15)
b = [root for root in roots if mp.im(root) == mp.mpf(0)][0]
bottom = b + mp.power(b, 2) / (wx + b)

print(
    "Print dimensions: {wx!s} x {wy!s}\n"
    "Resulting border: {b!s}\n"
    "Resulting bottom border: {bottom!s}"
    .format(wx=wx, wy=wy, b=b, bottom=bottom)
)

v = dict(
    mat_l=0 - b,
    mat_t=b,
    mat_w=wx + 2 * b,
    mat_h=-1 * (wy + b + bottom),
)
v['grid_l'] = 0 - mp.ceil(b)
v['grid_t'] = mp.ceil(b)
v['grid_w'] = mp.ceil(v['mat_w'])
v['grid_h'] = mp.ceil(v['mat_h'] - 1)


print(r"""
\begin{{tikzpicture}}
    \draw[help lines,very thin,color=blue!50!green!50,step=1] ({grid_l!s}, {grid_t!s}) grid +({grid_w!s}, {grid_h!s});
    % Mat
    \draw[fill=black,opacity=0.5] ({mat_l!s},{mat_t!s}) rectangle +({mat_w!s},{mat_h!s});
    % Window
    \draw[fill=white] (0,0) rectangle +(9,-6);
\end{{tikzpicture}}
""".format(**v))