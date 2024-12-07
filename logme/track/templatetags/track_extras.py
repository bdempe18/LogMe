from django import template

register = template.Library()


@register.filter
def get_field(form, field_name):
    return form.fields[field_name].get_bound_field(form, field_name)
