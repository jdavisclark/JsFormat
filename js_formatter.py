import sublime, sublime_plugin, re, sys, os

# crazyness to get jsbeautifier.unpackers to actually import
# with sublime's weird hackery of the path and module loading
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "jsbeaufifier"))
sys.path.append(os.path.join(directory, "jsbeautifier", "unpackers"))

# if you don't explicitly import jsbeautifier.unpackers here things will bomb out,
# even though we don't use it directly.....
import jsbeautifier, jsbeautifier.unpackers


s = sublime.load_settings("JsFormat.sublime-settings")

class PreSaveFormatListner(sublime_plugin.EventListener):
	"""Event listener to run JsFormat during the presave event"""
	def on_pre_save(self, view):
		fName = view.file_name()
		vSettings = view.settings()
		syntaxPath = vSettings.get('syntax')
		syntax = ""
		ext = ""

		if (fName != None): # file exists, pull syntax type from extension
			ext = os.path.splitext(fName)[1][1:]
		if(syntaxPath != None):
			syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()

		formatFile = "js" in ext or "json" in ext or "javascript" in syntax or "json" in syntax

		if(s.get("format_on_save") == True and formatFile):
			view.run_command("js_format")


class JsFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = self.view.settings()

		# settings
		opts = jsbeautifier.default_options()
		opts.indent_char = " " if settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(settings.get("tab_size")) if opts.indent_char == " " else 1
		opts.max_preserve_newlines = s.get("max_preserve_newlines") or 3
		opts.preserve_newlines = s.get("preserve_newlines") or True
		opts.jslint_happy = s.get("jslint_happy") or False
		opts.brace_style = s.get("brace_style") or "collapse"
		opts.keep_array_indentation = s.get("keep_array_indentation") or False
		opts.keep_function_indentation = s.get("keep_function_indentation") or False
		opts.indent_with_tabs = s.get("indent_with_tabs") or False
		opts.eval_code = s.get("eval_code") or False
		opts.unescape_strings = s.get("unescape_strings") or False
		opts.break_chained_methods = s.get("break_chained_methods") or False

		selection = self.view.sel()[0]
		nwsOffset = self.prev_non_whitespace()

		# do formatting and replacement
		replaceRegion = None
		formatSelection = False

		# formatting a selection/highlighted area
		if(len(selection) > 0):
			formatSelection = True
			replaceRegion = selection

		# formatting the entire file
		else:
			replaceRegion = sublime.Region(0, self.view.size())

		res = jsbeautifier.beautify(self.view.substr(replaceRegion), opts)
		if(not formatSelection and settings.get('ensure_newline_at_eof_on_save')):
			res = res + "\n"

		self.view.replace(edit, replaceRegion, res)

		# re-place cursor
		offset = self.get_nws_offset(nwsOffset, self.view.substr(sublime.Region(0, self.view.size())))
		rc = self.view.rowcol(offset)
		pt = self.view.text_point(rc[0], rc[1])
		sel = self.view.sel()
		sel.clear()
		self.view.sel().add(sublime.Region(pt))

		self.view.show_at_center(pt)


	def prev_non_whitespace(self):
		pos = self.view.sel()[0].a
		preTxt = self.view.substr(sublime.Region(0, pos));
		return len(re.findall('\S', preTxt))

	def get_nws_offset(self, nonWsChars, buff):
		nonWsSeen = 0
		offset = 0
		for i in range(0, len(buff)):
			offset += 1
			if not(buff[i].isspace()):
				nonWsSeen += 1

			if(nonWsSeen == nonWsChars):
				break

		return offset
