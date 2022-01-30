from django import template

register = template.Library()


@register.filter(name="seratus")
def seratus(value, arg):
    return value.replace(arg, "")
