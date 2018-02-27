#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

	# Specific settings for Heroku
	if 'IS_HEROKU' in os.environ:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EntHub.heroku_settings")
	else:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EntHub.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
