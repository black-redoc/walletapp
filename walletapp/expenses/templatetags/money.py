from django import template

register = template.Library()


@register.filter
def money(value: int) -> str:
    money_value = f"${float(value or 0):,.2f}"
    money_value = money_value.split(".")
    money_value = money_value[0].replace(",", ".") + "," + money_value[1]
    return money_value
