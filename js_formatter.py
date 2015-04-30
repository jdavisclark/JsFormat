import sublime, sublime_plugin, re, sys, os, json

directory = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(directory, "libs")
src_path = os.path.join(directory, "src")
is_py2k = sys.version_info < (3, 0)

# Python 2.x on Windows can't properly import from non-ASCII paths, so
# this code added the DOC 8.3 version of the lib folder to the path in
# case the user's username includes non-ASCII characters
def add_lib_path(lib_path):
	def _try_get_short_path(path):
		path = os.path.normpath(path)
		if is_py2k and os.name == 'nt' and isinstance(path, unicode):
			try:
				import locale
				path = path.encode(locale.getpreferredencoding())
			except:
				from ctypes import windll, create_unicode_buffer
				buf = create_unicode_buffer(512)
				if windll.kernel32.GetShortPathNameW(path, buf, len(buf)):
					path = buf.value
		return path
	lib_path = _try_get_short_path(lib_path)
	if lib_path not in sys.path:
		sys.path.append(lib_path)

# crazyness to get jsbeautifier.unpackers to actually import
# with sublime's weird hackery of the path and module loading
add_lib_path(libs_path)
add_lib_path(os.path.join(libs_path, "six-1.8.0"))
add_lib_path(os.path.join(libs_path, "jsbeautifier"))
add_lib_path(os.path.join(libs_path, "jsbeautifier", "jsbeautifier"))
add_lib_path(src_path)

import jsbeautifier, jsbeautifier.unpackers
import jsf, jsf_activation, jsf_rc

s = None

def plugin_loaded():
	global s
	s = sublime.load_settings("JsFormat.sublime-settings")

if is_py2k:
	plugin_loaded()


class PreSaveFormatListner(sublime_plugin.EventListener):
	"""Event listener to run JsFormat during the presave event"""
	def on_pre_save(self, view):
		if(s.get("format_on_save") == True and jsf_activation.is_js_buffer(view)):
			# only auto-format on save if there are no "lint errors"
			# here are some named regions from sublimelint see https://github.com/lunixbochs/sublimelint/tree/st3
			lints_regions = ['lint-keyword-underline', 'lint-keyword-outline']
			for linter in lints_regions:
				if len(view.get_regions(linter)):
					return
			view.run_command("js_format")

class JsFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = self.view.settings()

		# settings
		opts = jsbeautifier.default_options()
		opts.indent_char = " " if settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(settings.get("tab_size")) if opts.indent_char == " " else 1
		opts = jsf_rc.augment_options(opts, s)

		if(s.get("jsbeautifyrc_files") == True):
			opts = jsf_rc.augment_options_by_rc_files(opts, self.view)

		selection = self.view.sel()[0]

		# formatting a selection/highlighted area
		if(len(selection) > 0):
			jsf.format_selection(self.view, edit, opts)
		else:
			jsf.format_whole_file(self.view, edit, opts)

	def is_visible(self):
		return jsf_activation.is_js_buffer(self.view)
