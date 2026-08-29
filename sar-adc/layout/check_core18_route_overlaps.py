#!/usr/bin/env python3
"""Find accidental same-layer intersections among the 16 DAC top routes."""

from __future__ import annotations


CTL_Y = -14.1
P_XP = [-13.52, 1.22, 16.36, 31.90, 47.84, 64.38, 81.52, 99.26]
P_XS = [-14.32, 0.42, 15.56, 31.10, 47.04, 63.58, 82.50, 98.46]
P_XD = [194.6, 195.7, 196.8, 231.0, 201.8, 202.9, 206.7, 207.8]
N_XP = [289.78, 274.64, 259.10, 243.16, 226.62, 209.48, 191.74, 173.20]
N_XS = [288.98, 273.84, 258.30, 243.96, 225.82, 208.68, 192.50, 170.80]
N_XD = [212.7, 218.7, 224.7, 236.7, 242.7, 248.7, 254.7, 266.7]


def box(x1: float, y1: float, x2: float, y2: float):
    return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


def pad(x: float, y: float):
    return box(x - 0.2, y - 0.2, x + 0.2, y + 0.2)


def overlap(a, b) -> bool:
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


def route(name: str, yp: float, xd: float, yt: float, xp: float, xs: float):
    m3 = [
        box(186.6, yp - 0.2, xd + 0.2, yp + 0.2),
        pad(xd, yp), pad(xd, yt),
        box(xd - 0.2, yt - 0.2, xs + 0.2, yt + 0.2),
        pad(xs, yt), pad(xs, CTL_Y),
        box(xs - 0.2, CTL_Y - 0.2, xp + 0.2, CTL_Y + 0.2),
    ]
    m4 = [
        pad(xd, yp), box(xd - 0.2, yp, xd + 0.2, yt), pad(xd, yt),
        pad(xs, yt), box(xs - 0.2, yt, xs + 0.2, CTL_Y), pad(xs, CTL_Y),
    ]
    return {"name": name, "M3": m3, "M4": m4}


routes = []
for bit in range(8):
    routes.append(route(
        f"dac_code_n[{bit}]", 145.0 + 90.30 - 2.52 * bit,
        P_XD[bit], -55.0 - 1.3 * bit, P_XP[bit], P_XS[bit],
    ))
for bit in range(8):
    routes.append(route(
        f"dac_code[{bit}]", 145.0 + 70.14 - 2.52 * bit,
        N_XD[bit], -65.4 - 1.3 * bit, N_XP[bit], N_XS[bit],
    ))

found = False
for left_index, left in enumerate(routes):
    for right in routes[left_index + 1:]:
        for layer in ("M3", "M4"):
            for left_box in left[layer]:
                for right_box in right[layer]:
                    if overlap(left_box, right_box):
                        print(
                            left["name"], right["name"], layer,
                            left_box, right_box,
                        )
                        found = True
if not found:
    print("No cross-net M3/M4 route overlaps.")
