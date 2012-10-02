import sublime, sublime_plugin, jsbeautifier, re

s = sublime.load_settings("JsFormat.sublime-settings")

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
		opts.space_before_line_starters = s.get("space_before_line_starters") or False

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