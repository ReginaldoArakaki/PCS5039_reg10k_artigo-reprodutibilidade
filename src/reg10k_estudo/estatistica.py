"""Estatística descritiva sem dependência de bibliotecas numéricas."""
from __future__ import annotations

import math
import statistics


def media(valores):
    xs = [float(x) for x in valores if x is not None]
    return round(statistics.fmean(xs), 4) if xs else None


def pearson(x, y):
    pares = [(float(a), float(b)) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pares) < 3:
        return None
    xs, ys = zip(*pares)
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    numerador = sum((a - mx) * (b - my) for a, b in pares)
    denominador = math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
    return round(numerador / denominador, 4) if denominador else None
