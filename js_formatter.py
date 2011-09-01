import sublime, sublime_plugin, jsbeautifier

class JsFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		opts = jsbeautifier.default_options();
		opts.indent_char = " "
		opts.indent_size = 4
		opts.max_preserve_newlines = 3
		selection = self.view.sel()[0]
		replaceRegion = selection if len(selection) > 0 else sublime.Region(0, self.view.size())
		res = jsbeautifier.beautify(self.view.substr(replaceRegion), opts)
		prePos = self.view.sel()[0]
		self.view.replace(edit, replaceRegion, res)
		self.view.show_at_center(prePos.begin())
		
