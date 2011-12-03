import sublime, sublime_plugin, jsbeautifier

class JsFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = self.view.settings()
		opts = jsbeautifier.default_options()
		opts.indent_char = " " if settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(settings.get("tab_size")) if opts.indent_char == " " else 1 
		opts.max_preserve_newlines = 3
		selection = self.view.sel()[0]
		replaceRegion = selection if len(selection) > 0 else sublime.Region(0, self.view.size())
		res = jsbeautifier.beautify(self.view.substr(replaceRegion), opts)
		prePos = self.view.sel()[0]
		self.view.replace(edit, replaceRegion, res)
		self.view.show_at_center(prePos.begin())
		
