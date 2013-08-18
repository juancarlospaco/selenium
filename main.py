# -*- coding: utf-8 -*-
# PEP8:NO, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Selenium Ninja "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 20/08/2013 '
__prj__ = ' selenium '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from sip import setapi
from datetime import datetime
from getpass import getuser

from PyQt4.QtGui import (QLabel, QCompleter, QDirModel, QPushButton, QWidget,
  QFileDialog, QDockWidget, QVBoxLayout, QCursor, QLineEdit, QIcon, QGroupBox,
  QCheckBox, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QColor, QComboBox,
  QMessageBox, QScrollArea, QSpinBox)

from PyQt4.QtCore import Qt, QDir

try:
    from os import startfile
except ImportError:
    from subprocess import Popen

try:
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
except ImportError:
    from PyQt4.QtGui import QPlainTextEdit  # lint:ok

from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin


from selenium_template import SELENIUM_TEMPLATE, HEADER


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constans
HELPMSG = '''
<h3>Selenium Ninja</h3>
This tool combines the following Technologies on Ninja-IDE.
<ul>
<li>Write and Run Tests by itself.
<li>Generate Boilerplate Code for Tests.
<li><a href="http://docs.seleniumhq.org">Selenium Tests</a>
<li><a href="http://nose.readthedocs.org">Nose Easy Testing Framework</a>
<li><a href="http://splinter.cobrateam.info">Splinter Testing Framework for Web
</a></ul>
<a href="http://www.w3.org/TR/webdriver"><b>Selenium API is a 3W Web Standard.
</a>
<br><br><i>This plugin is Beta.</i><br><br>
''' + ''.join((__doc__, __version__, __license__, 'by', __author__, __email__))

HEADER = HEADER.format(getuser(), datetime.today().isoformat().split('.')[0])


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        ec = ExplorerContainer()
        super(Main, self).initialize(*args, **kwargs)
        # directory auto completer
        self.completer, self.dirs = QCompleter(self), QDirModel(self)
        self.dirs.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.RUNS, self.FAILS = 0, 0
        self.group0 = QGroupBox()
        self.group0.setTitle(' Source and Target ')
        self.baseurl = QLineEdit('http://google.com')
        self.outfile = QLineEdit(path.join(path.expanduser("~"), 'test.py'))
        self.outfile.setCompleter(self.completer)
        self.open = QPushButton(QIcon.fromTheme("folder-open"), 'Open')
        self.open.clicked.connect(lambda: self.outfile.setText(
            QFileDialog.getSaveFileName(self.dock, "Save", path.expanduser("~"),
            'PYTHON(*.py)')))
        vboxg0 = QVBoxLayout(self.group0)
        for each_widget in (QLabel('<b>Base URL'), self.baseurl,
            QLabel('<b>Local File Target'), self.outfile, self.open):
            vboxg0.addWidget(each_widget)

        self.group1 = QGroupBox()
        self.group1.setTitle(' Selenium ')
        self.group1.setCheckable(True)
        self.group1.setGraphicsEffect(QGraphicsBlurEffect(self))
        self.group1.graphicsEffect().setEnabled(False)
        self.group1.toggled.connect(self.toggle_group)
        self.ckcss1 = QCheckBox('Test for correct Page Loading behaviour')
        self.ckcss2 = QCheckBox('Test for Sucessfull Status Code return')
        self.ckcss3 = QCheckBox('Test for valid Title of the web page')
        self.ckcss4 = QCheckBox('Test for Cookies Basic functionality')
        self.ckcss5 = QCheckBox('Test for Back, Forward, Reload behaviour')
        self.ckcss6 = QCheckBox('Take a Screenshot of page (CSS Debug)')
        self.ckcss7 = QCheckBox('Test for Search Form Field of the page')
        self.ckcss8 = QCheckBox('Test for Arbitrary Javascript (User provided)')
        self.ckcss9 = QCheckBox('Test for iFrame of the web page')
        self.ckcss10 = QCheckBox('Test for HTML5 Canvas element on the page')
        self.ckcss11 = QCheckBox('Test for HTML5 SVG element on the page')
        self.ckcss12 = QCheckBox('Test for HTML5 Audio element on the page')
        self.ckcss13 = QCheckBox('Test for HTML5 Video element on the page')
        self.ckcss14 = QCheckBox('Test for File Upload form on the page')
        self.ckcss15 = QCheckBox('Add ChromeDriver path to sys.path')
        self.webdriver = QComboBox()
        self.webdriver.addItems(['firefox', 'chrome',
                                 'zope.testbrowser', 'phantomjs'])
        self.titletxt = QLineEdit('Google')
        self.javascript = QLineEdit('console.log("test")')
        self.authdata, self.formdata = QLineEdit(), QLineEdit()
        self.authdata.setPlaceholderText("{'username':'root','password':'123'}")
        self.formdata.setPlaceholderText("{'name': 'Joe', 'age': '25'}")
        self.iframurl = QLineEdit()
        self.chrmedrv = QLineEdit('/usr/bin/chromedriver')
        self.timeout = QSpinBox()
        self.timeout.setMaximum(99)
        self.timeout.setMinimum(0)
        self.timeout.setValue(9)
        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (self.ckcss1, self.ckcss2, self.ckcss3, self.ckcss4,
            self.ckcss5, self.ckcss6, self.ckcss7, self.ckcss8, self.ckcss9,
            self.ckcss10, self.ckcss11, self.ckcss12, self.ckcss13,
            self.ckcss14, self.ckcss15, QLabel('<b>WebDriver'), self.webdriver,
            QLabel('''<center><small><i>Firefox is only Driver that dont
                   require additional configuration'''),
            QLabel('<b>Title Content must contain'), self.titletxt,
            QLabel('<b>Minified Javascript for Test'), self.javascript,
            QLabel('<b>Arbitrary Authentication Data for Test'), self.authdata,
            QLabel('<b>Arbitrary Form Data for Test'), self.formdata,
            QLabel('<b>iFrame URL for Test'), self.iframurl,
            QLabel('<b>Chrome Driver'), self.chrmedrv,
            QLabel('<b>Timeout Timer Limit'), self.timeout):
            vboxg1.addWidget(each_widget)
            try:
                each_widget.setToolTip(each_widget.text())
            except:
                each_widget.setToolTip(each_widget.currentText())

        self.group4 = QGroupBox()
        self.group4.setTitle(' General ')
        self.chckbx1 = QCheckBox('Run the Tests after Writing')
        self.chckbx2 = QCheckBox('Open the Tests with Ninja after Writing')
        self.chckbx3 = QCheckBox('Add SheBang, Encoding and Metadata to Tests')
        self.nice = QSpinBox()
        self.nice.setMaximum(20)
        self.nice.setMinimum(0)
        self.nice.setValue(20)
        self.help1 = QLabel('''<a href="http://splinter.cobrateam.info/docs/api"
            ><center><b>API Reference</a>''')
        self.help1.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.help1.setOpenExternalLinks(True)
        vboxg4 = QVBoxLayout(self.group4)
        for each_widget in (self.chckbx1, self.chckbx2, self.chckbx3,
            QLabel('Backend CPU priority:'), self.nice, self.help1):
            vboxg4.addWidget(each_widget)
            each_widget.setToolTip(each_widget.text())

        [a.setChecked(True) for a in (self.ckcss1, self.ckcss2, self.ckcss3,
            self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7, self.ckcss8,
            self.ckcss15, self.chckbx1, self.chckbx2, self.chckbx3)]

        self.button = QPushButton(QIcon.fromTheme("face-cool"),
                                  'Write and Run Test')
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setMinimumSize(100, 50)
        self.button.clicked.connect(self.run)
        glow = QGraphicsDropShadowEffect(self)
        glow.setOffset(0)
        glow.setBlurRadius(99)
        glow.setColor(QColor(99, 255, 255))
        self.button.setGraphicsEffect(glow)
        glow.setEnabled(True)
        self.output = QPlainTextEdit()
        self.runs = QLabel('<font color="green"><b>Runs: 0')
        self.failures = QLabel('<font color="red"><b>Failures: 0')

        class TransientWidget(QWidget):
            ' persistant widget thingy '
            def __init__(self, widget_list):
                ' init sub class '
                super(TransientWidget, self).__init__()
                vbox = QVBoxLayout(self)
                for each_widget in widget_list:
                    vbox.addWidget(each_widget)

        tw = TransientWidget((QLabel('<b>Selenium Tests'), self.group0,
            self.group1, self.group4, QLabel('<b>Log'), self.output, self.runs,
            self.failures, self.button))
        self.scrollable, self.dock = QScrollArea(), QDockWidget()
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(tw)
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.dock.setWidget(self.scrollable)
        ec.addTab(self.dock, "Selenium")
        QPushButton(QIcon.fromTheme("help-about"), 'About', self.dock
          ).clicked.connect(lambda: QMessageBox.information(self.dock, __doc__,
            HELPMSG))
        QPushButton(QIcon.fromTheme("media-record"), 'Record', self.group1,
          ).clicked.connect(lambda: QMessageBox.information(self.dock, __doc__,
        'Not working. If you know how to make it Record, send me Pull Request'))

    def run(self):
        ' run '
        self.RUNS = self.RUNS + 1
        self.runs.setText('<font color="green"><b>Runs: {}'.format(self.RUNS))
        self.output.clear()
        self.output.append(self.formatInfoMsg('INFO:{}'.format(datetime.now())))
        self.button.setDisabled(True)
        self.output.append(self.formatInfoMsg(' INFO: OK: Parsing Data '))
        selenium_test = SELENIUM_TEMPLATE.format(
            HEADER if self.chckbx3.isChecked() is True else '',
            self.chrmedrv.text() if self.ckcss15.isChecked() is True else '',
            self.baseurl.text(),
            self.authdata.text() if str(self.authdata.text()) is not '' else {},
            self.formdata.text() if str(self.formdata.text()) is not '' else {},
            self.iframurl.text(), self.javascript.text(), self.titletxt.text(),
            self.webdriver.currentText(),
            '# ' if self.ckcss1.isChecked() is not True else '',
            '# ' if self.ckcss2.isChecked() is not True else '',
            '# ' if self.ckcss2.isChecked() is not True else '',
            '# ' if self.ckcss3.isChecked() is not True else '',
            '# ' if self.ckcss4.isChecked() is not True else '',
            '# ' if self.ckcss5.isChecked() is not True else '',
            '# ' if self.ckcss6.isChecked() is not True else '',
            '# ' if self.ckcss7.isChecked() is not True else '',
            '# ' if self.ckcss8.isChecked() is not True else '',
            '# ' if self.ckcss9.isChecked() is not True else '',
            '# ' if self.ckcss10.isChecked() is not True else '',
            '# ' if self.ckcss11.isChecked() is not True else '',
            '# ' if self.ckcss12.isChecked() is not True else '',
            '# ' if self.ckcss13.isChecked() is not True else '',
            '# ' if self.ckcss14.isChecked() is not True else '',
            self.timeout.value()
            )
        with open(path.abspath(self.outfile.text()), 'w') as f:
            self.output.append(self.formatInfoMsg(' INFO: OK: Writing Tests '))
            f.write(selenium_test)
        if self.chckbx2.isChecked() is True:
            self.output.append(self.formatInfoMsg(' INFO: OK: Opening Tests '))
            try:
                startfile(str(path.abspath(self.outfile.text())))
            except:
                Popen(["ninja-ide", str(path.abspath(self.outfile.text()))])
        if self.chckbx1.isChecked() is True:
            try:
                self.output.append(self.formatInfoMsg('INFO: OK: Runing Tests'))
                Popen(["python", str(path.abspath(self.outfile.text()))])
            except:
                self.output.append(self.formatErrorMsg('INFO:FAIL: Tests Fail'))
                self.FAILS = self.FAILS + 1
                self.failures.setText(
                    '<font color="red"><b>Failures: {}'.format(self.FAILS))
        self.output.append(self.formatInfoMsg('INFO:{}'.format(datetime.now())))
        self.button.setDisabled(False)
        self.output.setFocus()
        self.output.selectAll()

    def toggle_group(self):
        ' toggle on or off the css checkboxes '
        if self.group1.isChecked() is True:
            [a.setChecked(True) for a in (self.ckcss1, self.ckcss2, self.ckcss3,
            self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7, self.ckcss8,
            self.ckcss15)]
            self.group1.graphicsEffect().setEnabled(False)
        else:
            [a.setChecked(False) for a in (self.ckcss1, self.ckcss2,
            self.ckcss3, self.ckcss4, self.ckcss5, self.ckcss6, self.ckcss7,
            self.ckcss8, self.ckcss15)]
            self.group1.graphicsEffect().setEnabled(True)

    def formatErrorMsg(self, msg):
        """Format error messages in red color"""
        return self.formatMsg(msg, 'red')

    def formatInfoMsg(self, msg):
        """Format informative messages in blue color"""
        return self.formatMsg(msg, 'green')

    def formatMsg(self, msg, color):
        """Format message with the given color"""
        return '<font color="{}">{}</font>'.format(color, msg)


###############################################################################


if __name__ == "__main__":
    print(__doc__)
