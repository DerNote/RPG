from django import template

register = template.Library()

@register.filter(name='get_form_field')
def get_form_field(form, field_name):
    field = form.fields[field_name]
    return form[field_name] if field else None

@register.filter(name='filter_fields_by_prefix')
def filter_fields_by_prefix(form, prefix):
    filtered_fields = {k: v for k, v in form.fields.items() if k.startswith(prefix)}
    return filtered_fields

