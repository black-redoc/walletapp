from random import shuffle
from typing import Any


def get_model_with_kind_property(sequence: Any, kind: str):
    """
    Get_model_with_kind_property() adds kind of transaction str property.

    Examples:
    --------
    >>>> obj = add_kind(income_obj, "income")
    >>>> obj.kind
    'income'
    """

    def closure(obj, kind_: str):
        obj.kind = kind_
        return obj

    return [closure(element, kind) for element in sequence]


def get_total_amount(sequence) -> int:
    """
    Get the sum of income amount or expense amount from a sequence.
    """
    return sum(map(lambda element: element.amount, sequence))


def get_flatten_lists(a, b, c):
    """
    Get many lists flatten to render in dashboard template togeter.
    """
    obj_list = list(a) + list(b) + list(c)
    shuffle(obj_list)
    return obj_list
