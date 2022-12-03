from functools import reduce
from operator import iconcat
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


def get_flatten_lists(*sequences: list[Any]) -> list[Any]:
    """
    Get many lists flatten to render in dashboard template togeter.
    """
    obj_list = zip(*sequences)
    return reduce(iconcat, obj_list, [])
