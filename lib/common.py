# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING

import locale
import gettext

APP = 'PyQuil'
DIR = 'locale'

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext
