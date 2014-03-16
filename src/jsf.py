import sublime, re

# if you don't explicitly import jsbeautifier.unpackers here things will bomb out,
# even though we don't use it directly.....
import jsbeautifier, jsbeautifier.unpackers
import merge_utils

def format_selection(view, edit, opts):
	def get_line_indentation_pos(view, point):
		line_region = view.line(point)
		pos = line_region.a
		end = line_region.b
		while pos < end:
			ch = view.substr(pos)
			if ch != ' ' and ch != '\t':
				break
			pos += 1
		return pos

	def get_indentation_count(view, start):
		indent_count = 0
		i = start - 1
		while i > 0:
			ch = view.substr(i)
			scope = view.scope_name(i)
			# Skip preprocessors, strings, characaters and comments
			if 'string.quoted' in scope or 'comment' in scope or 'preprocessor' in scope:
				extent = view.extract_scope(i)
				i = extent.a - 1
				continue
			else:
				i -= 1

			if ch == '}':
				indent_count -= 1
			elif ch == '{':
				indent_count += 1
		return indent_count

	regions = []
	for sel in view.sel():
		start = get_line_indentation_pos(view, min(sel.a, sel.b))
		region = sublime.Region(
			view.line(start).a,  # line start of first line
			view.line(max(sel.a, sel.b)).b)  # line end of last line
		indent_count = get_indentation_count(view, start)
		# Add braces for indentation hack
		code = '{' * indent_count
		if indent_count > 0:
			code += '\n'
		code += view.substr(region)
		# Performing astyle formatter
		formatted_code = jsbeautifier.beautify(code, opts)
		if indent_count > 0:
			for _ in range(indent_count):
				index = formatted_code.find('{') + 1
				formatted_code = formatted_code[index:]
			formatted_code = re.sub(r'[ \t]*\n([^\r\n])', r'\1', formatted_code, 1)
		else:
			# HACK: While no identation, a '{' will generate a blank line, so strip it.
			search = "\n{"
			if search not in code:
				formatted_code = formatted_code.replace(search, '{', 1)
		# Applying formatted code
		view.replace(edit, region, formatted_code)
		# Region for replaced code
		if sel.a <= sel.b:
			regions.append(sublime.Region(region.a, region.a + len(formatted_code)))
		else:
			regions.append(sublime.Region(region.a + len(formatted_code), region.a))
	view.sel().clear()
	# Add regions of formatted code
	[view.sel().add(region) for region in regions]

def format_whole_file(view, edit, opts):
	settings = view.settings()
	region = sublime.Region(0, view.size())
	code = view.substr(region)
	formatted_code = jsbeautifier.beautify(code, opts)

	if(settings.get("ensure_newline_at_eof_on_save") and not formatted_code.endswith("\n")):
		formatted_code = formatted_code + "\n"

	_, err = merge_utils.merge_code(view, edit, code, formatted_code)
	if err:
		sublime.error_message("JsFormat: Merge failure: '%s'" % err)