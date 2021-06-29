def value_is_nan(
        value) \
        -> bool:
    if isinstance(value, float):
        import math

        return \
            math.isnan(
                value)

    else:
        return \
            False

