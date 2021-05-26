BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALPHABET_LEN = len(BASE62_ALPHABET)


def int_to_base62(value):
    """
    Convert int value to a base62 string.
    """
    if value == 0:
        return "0"

    chars = []
    while value > 0:
        value, remainder = divmod(value, ALPHABET_LEN)
        chars.append(BASE62_ALPHABET[remainder])

    return ''.join(reversed(chars))


def shorten_url(url, db_wrapper):
    # we already have a short version of this, so return it
    if (short := db_wrapper.lookup_url(url)) is not None:
        return short

    # create the new shortend version
    # TODO - in practice, we would want a much better shortened version, but in the interest of time...
    short = int_to_base62(hash(url))

    # remember it
    db_wrapper.add(url, short)

    return short
