"""
Copyright (c) 2012 The GoSublime Authors

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
"""

# Borrowed from GoSublime

import sublime

from .diff_match_patch import diff_match_patch


class MergeException(Exception):
    pass


def _merge_code(view, edit, code, formatted):
    def ss(start, end):
        return view.substr(sublime.Region(start, end))

    dmp = diff_match_patch()
    diffs = dmp.diff_main(code, formatted)
    dmp.diff_cleanupEfficiency(diffs)
    i = 0
    dirty = False
    for k, s in diffs:
        l = len(s)
        if k == 0:
            # match
            l = len(s)
            if ss(i, i + l) != s:
                raise MergeException('mismatch', dirty)
            i += l
        else:
            dirty = True
            if k > 0:
                # insert
                view.insert(edit, i, s)
                i += l
            else:
                # delete
                if ss(i, i + l) != s:
                    raise MergeException('mismatch', dirty)
                view.erase(edit, sublime.Region(i, i + l))
    return dirty


def merge_code(view, edit, code, formatted_code):
    vs = view.settings()
    ttts = vs.get("translate_tabs_to_spaces")
    vs.set("translate_tabs_to_spaces", False)
    if not code.strip():
        return (False, '')

    dirty = False
    err = ''
    try:
        dirty = _merge_code(view, edit, code, formatted_code)
    except MergeException as err:
        dirty = True
        err = "Could not merge changes into the buffer, edit aborted: %s" % err
        view.replace(edit, sublime.Region(0, view.size()), code)
    except Exception as ex:
        err = "Unknown exception: %s" % ex
    finally:
        vs.set("translate_tabs_to_spaces", ttts)
        return (dirty, err)
