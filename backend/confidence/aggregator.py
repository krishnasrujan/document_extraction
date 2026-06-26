import math

def weighted_geometric_mean(signals):
    total_weight = sum(
        signal["weight"]
        for signal in signals
    )

    score = 0

    for signal in signals:
        score += (
            signal["weight"]
            *
            math.log(
                max(
                    signal["score"],
                    0.001
                )
            )
        )

    return math.exp(
        score / total_weight
    )