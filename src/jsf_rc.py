import os, json, sublime

def get_rc_paths(cwd):
	result = []
	subs = cwd.split(os.sep)
	fullPath = ""

	for value in subs:
		fullPath += value + os.sep
		result.append(fullPath + '.jsbeautifyrc')

	return result

def filter_existing_files(paths):
	result = []

	for value in paths:
		if (os.path.isfile(value)):
			result.append(value)

	return result

def read_json(path):
	f = open(path, 'r');
	result = None

	try:
		result = json.load(f);
	except:
		sublime.error_message("JsFormat Error.\nInvalid JSON: " + path)
	finally:
		f.close();

	return result

def augment_options(options, subset):
	"""	augment @options with defined values in @subset

		options -- a regular old class with public attributes
	   	subset -- anything with a 'get' callable (json style)
	"""
	fields = [attr for attr in dir(options) if not callable(getattr(options, attr)) and not attr.startswith("__")]

	for field in fields:
		value = subset.get(field)
		if value != None:
			setattr(options, field, value)

	return options

def augment_options_by_rc_files(options, view):
	fileName = view.file_name()

	if (fileName != None):
		files = filter_existing_files(get_rc_paths(os.path.dirname(fileName)))
		for value in files:
			jsonOptions = read_json(value)
			options = augment_options(options, jsonOptions)

	return options
