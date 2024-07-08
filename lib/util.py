import math


def parse_score(score):
    if math.isfinite(score):
        return score
    is_positive_infinity = score > 0
    return "-∞" if not is_positive_infinity else "∞"
