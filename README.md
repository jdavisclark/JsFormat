## Summary
JsFormat is a javascipt formatting plugin for Sublime Text 2.
It uses the commandline/python-module javascript formatter from http://jsbeautifier.org/ to format the selected text, 
or the entire file if there is no selection. The plugin does not check to make sure the buffer has a ".js" file type, 
it just javascript formats the selection/file. Thus, use with caution if you are in an html file.


## Features
* javascript/json formatting (obviously)
* all settings are customizable (whitespace, formatting style, etc..)
* puts the cursor back in the same location it was before formatting (accounts for whitespace/newline changes)

## Settings
JsFormat uses whatever tab character settings are configured with the standard "translate_tabs_to_spaces" and "tab_size" sublime settings.

In addition, the following settings are available in JsFormat/JsFormat.sublime-settings (defaults shown below):

* "max_preserve_newlines": 4
* "preserve_newlines": true
* "jslint_happy": false
* "brace_style": "collapse"
* "keep_array_indentation": false
* "keep_function_indentation": false
* "indent_with_tabs": false
* "ensure_newline_at_eof_on_save": false
* "space_before_line_starters": false

## Install
#### [Package Control](https://github.com/wbond/sublime_package_control) (*Recommended*)
JsFormat is now included in the default repository channel for [Package Control](https://github.com/wbond/sublime_package_control). It should show up in your install list
with no changes.

If it does not show up, or you are on an older version of Package Control:
Add https://github.com/jdc0589/JsFormat as a Package Control repository. JsFormat will show up in the
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

[This is the current bug report we are using to discuss this issue](https://github.com/jdc0589/JsFormat/issues/7); in addition I have made a [wiki page here](https://github.com/jdc0589/JsFormat/wiki/Plugins-With-Conflicting-Keybindings) to document offending plugins. If we find all the offending plugins, I will be more than happy to contribute to them to fix the problem.

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
