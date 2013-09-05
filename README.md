## Summary
JsFormat is a javascript formatting plugin for Sublime Text 2.
It uses the command-line/python-module javascript formatter from http://jsbeautifier.org/ to format whole js or json files, or the selected portion(s).


## Features
* javascript/json formatting (obviously)
* all settings are customizable (whitespace, formatting style, etc..)
* .jsbeautifyrc settings files support for even more control on a per-project basis
* puts the cursor back in the same location it was before formatting (accounts for whitespace/newline changes)
* Sublime Text 3 support


## Settings
JsFormat uses whatever tab/indent settings are configured with the standard ```translate_tabs_to_spaces``` and ```tab_size``` sublime settings.

The following **JsBeautifier** settings are available in JsFormat/JsFormat.sublime-settings (defaults shown below). Check out the official [jsbeautifier documentation](https://github.com/einars/js-beautify#options) for more details on the options:

* `indent_with_tabs`: false
* `max_preserve_newlines`: 4
* `preserve_newlines`: true
* `space_in_paren`: false
* `jslint_happy`: false
* `brace_style`: "collapse"
* `keep_array_indentation`: false
* `keep_function_indentation`: false
* `eval_code`: false,
* `unescape_strings`: false,
* `break_chained_methods`: false*
* `e4x`: false
* `wrap_line_length`: 0

The following **JsFormat** specific settings are also exposed:

- `format_on_save`: false  (format files on buffer save)
- `jsbeautifyrc_files`: false (see the [.jsbeautifyrc files](#jsbeautifyrc-files) section)

I had temporary lapse of judgment a while back and merged a pull request that modified jsbeautifier. As a result, the functionality that
was added from that pull request has been lost; ```"ensure_space_before_linestarters"``` is no longer supported.

The JsFormat specific ```ensure_newline_at_eof_on_save``` setting has also been removed. This functionality exists in sublime core.

#### jsbeautifyrc files ####
JsFormat now supports `.jsbeautifyrc` JSON files (disabled by default), which themselves support any of the exposed JsBeautifier options. The option augmentation order is: default options -> user settings -> `.jsbeautifyrc` option files. 

A hierarchy of `.jsbeautifyrc` files is supported, where rc files at the deeper levels override the settings from rc files at higher levels. For example, given the file structure listed below, formatting `/home/you/myProject/app.js` would inherit settings from: default -> user settings -> `/home/you/myProject/.jsbeautifyrc`, while formatting `/home/you/myProject/tests/test.js` would inherit settings from: default -> user settings -> `/home/you/myProject/.jsbeautifyrc` -> `/home/you/myProject/tests/.jsbeautifyrc` 

- /home/you/myProject/.jsbeautifyrc
- /home/you/myProject/app.js
- /home/you/myProject/tests/.jsbeautifyrc
- /home/you/myProject/tests/test.js  



## Install
#### [Package Control](https://github.com/wbond/sublime_package_control) (Recommended)
JsFormat is now included in the default repository channel for [Package Control](https://github.com/wbond/sublime_package_control). It should show up in your install list
with no changes.

If it does not show up, or you are on an older version of Package Control,
add https://github.com/jdc0589/JsFormat as a Package Control repository. JsFormat will show up in the
package install list.

#### Git Clone
Clone this repository in to the Sublime Text 2 "Packages" directory, which is located where ever the
"Preferences" -> "Browse Packages" option in sublime takes you.




## Key Binding

The default key binding is "ctrl+alt+f"

## Key Binding Conflicts

Unfortunately there are other plugins that use "ctrl + alt + f", this is a hard problem to solve. If JsFormat works
OK via the command palette but does nothing when you use the "ctrl + alt + f" shortcut, you have two options:

1. Add ```{ "keys": ["ctrl+alt+f"], "command": "js_format"}``` to your user keybindings file. This will override anything specifid by a plugin.
2. Find the offending plugin, and change the shortcut in its sublime-keymap file (will revert on updates)


## Command Palette

Open the command palette via "ctrl + shift + p", Jsformat appears as "Format: Javascript"

---

### License
Copyright (C) 2012 Davis Clark

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
