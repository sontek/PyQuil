# A Database and Query Analyze Tool
# Copyright (c) 2010-2011 John Anderson <sontek@gmail.com>
# License: GPLv3. See COPYING

from lib.common import _

def get_plugin(name):
    plugin = None

    if name == _('Sql Alchemy'):
        from plugins.sqlalchemy import SAQueryPlugin
        plugin = SAQueryPlugin()
    elif name == _('MSSQL'):
        from plugins.mssql import MSSQLQueryPlugin
        plugin = MSSQLQueryPlugin()

    return plugin

