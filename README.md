### Summary

Uses the commandline/python-module javascript formatter from http://jsbeautifier.org/ to format the selected text, or the entire file if there is no selection. Plugin does not check to make sure the buffer has a ".js" file type, it just javascript formats the selection/file. Thus, use with caution if you are in an html file.

### Install

Extract the download archive, paste the JsBeautifier folder in the Sublime Text 2 "Packages" directory, which is located where ever the "Preferences" -> "Browse Packages" option in sublime takes you.

### Key Binding

The default key binding is "ctrl+alt+f"

## Updates
* 8/25/2011 - Added sublime-commands file. "Format: Javascript" now appears in the command palette
* 8/25/2011 - scrolls back to whatever line you were on prior to formatting the file (middle of screen) rather than leaving the view position at the top of the file after formatting.