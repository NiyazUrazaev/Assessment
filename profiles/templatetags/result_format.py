from django import template

register = template.Library()


@register.filter
def percentage(arg):
    return f"{int(float(arg) * 100)}%"


@register.filter
def table_class(arg):
    result = float(arg) * 100
    if result >= 80:
        return 'table-success'
    elif 50 < result < 80:
        return 'table-warning'
    else:
        return 'table-danger'


@register.filter
def in_minutes(arg):
    return round(arg.seconds / 60)


@register.filter
def seconds(arg):
    return arg.seconds % 60
