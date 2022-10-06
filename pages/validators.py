from django.core.exceptions import ValidationError


def exclude_slash(value: str):
	if '/' in value:
		raise ValidationError('No slashes ("/") allowed!')
