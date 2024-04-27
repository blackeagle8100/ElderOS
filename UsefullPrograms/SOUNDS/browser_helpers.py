#!/usr/bin/env python3

import os.path
import tempfile
import webbrowser

ASSISTANT_HTML_FILE = 'google-assistant-sdk-screen-out.html'


class SystemBrowser(object):
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()
        self.filename = os.path.join(self.tempdir, ASSISTANT_HTML_FILE)

    def display(self, html):
        with open(self.filename, 'wb') as f:
            f.write(html)
        webbrowser.open(self.filename, new=0)


system_browser = SystemBrowser()
