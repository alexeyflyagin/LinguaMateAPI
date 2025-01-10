def raise_exception_if_none(it, e):
    if e is not None and it is None:
        raise e


def raise_exception_if_not_none(it, e):
    if e is not None and it is not None:
        raise e
