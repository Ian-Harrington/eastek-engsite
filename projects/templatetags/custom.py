import datetime
from django import template


register = template.Library()

@register.filter
def human_readable(value, arg):
	"""converts database values to their human readable form"""
	for pair in arg:
		if value == pair[0]:
			return pair[1]
	else:
		return value 

@register.filter
def future(value):
	"""consumes a date or datetime, and checks if the date is in the future"""
	try:
		date = datetime.date(year=value.year, month=value.month, day=value.day)
	except AttributeError:
		return None
	return date > datetime.date.today()

@register.filter
def past(value):
	"""consumes a date or datetime, and checks if the date is in the past"""
	try:
		date = datetime.date(year=value.year, month=value.month, day=value.day)
	except AttributeError:
		return None
	return date < datetime.date.today()

@register.filter
def verbose_name(model, field):
	"""consumes a model field and returns the verbose name"""
	try:
		return model._meta.get_field(str(field)).verbose_name
	except AttributeError:
		return str(field)