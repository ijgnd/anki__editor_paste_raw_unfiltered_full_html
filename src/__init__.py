"""
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
Copyright: 2020- ijgnd


This add-on uses Octicons-diff-ignored.svg which
is covered by the following copyright and permission notice:

    MIT License

    Copyright (c) 2019 GitHub Inc.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

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

import os

from anki.hooks import wrap, addHook
from anki.utils import stripHTMLMedia

from aqt import mw
from aqt.editor import Editor
from aqt.qt import *


addon_path = os.path.dirname(__file__)
unique_string = 'äöüäöüzuio'


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail


def _myRawPaste(self, html, field):
    f = self.note.fields
    before, after = f[field].split(unique_string)
    f[field] = before + html + after
    self.note.flush()
    self.loadNote(focusTo=field)


def myRawPaste(self):
    field = self.currentField
    mode = QClipboard.Clipboard
    mime = self.mw.app.clipboard().mimeData(mode=mode)
    html, internal = self.web._processMime(mime)
    if not html:
        return
    self.web.eval("""setFormat("insertText", "%s");""" % unique_string)
    self.saveNow(lambda e=self, h=html, i=field: _myRawPaste(e, h, i))


if gc("show button"):
    def keystr(k):
        key = QKeySequence(k)
        return key.toString(QKeySequence.NativeText)
    def setupEditorButtonsFilterFD(buttons, editor):
        b = editor.addButton(
            os.path.join(addon_path, "Octicons-diff-ignored.svg"),
            "paste_unfiltered_button",
            lambda e=editor: myRawPaste(e, False),
            tip="Paste unfiltered/full html ({})".format(keystr(gc("full html shortcut", ""))),
            keys=gc("fullhtml_shortcut", "")
            )
        buttons.extend([b])
        return buttons
    addHook("setupEditorButtons", setupEditorButtonsFilterFD)
else:
    def SetupShortcuts(cuts, editor):
        fh = gc("fullhtml_shortcut")
        if fh:
            cuts.append((fh, lambda e=editor: myRawPaste(e, False)))
    addHook("setupEditorShortcuts", SetupShortcuts)
