#!/usr/bin/env python
# coding=utf-8
# ---------------------------------------------------------------------------
# Messages compiler for Ajenti plugins.
#
#   Copyright (C) 2015 Marc Bertens <m.bertens@pe2mbs.nl>
#   Adapted from make_messages.py by Eugene Pankov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see http://www.gnu.org/licenses/agpl-3.0.html.
# ---------------------------------------------------------------------------
#
import os
import sys
import subprocess
from lxml import etree

def check_call(*args):
    try:
        subprocess.call(*args)
    except Exception as e:
        print('Call failed')
        print(' '.join(args[0]))
        print(str(e))


LOCALEDIR = 'locales'
LANGUAGES = [x for x in os.listdir(LOCALEDIR) if not '.' in x]

pot_path = os.path.join(LOCALEDIR, 'ajenti.po')

if len(sys.argv) != 2:
    print('Usage: ./make_messages.py [extract|compile]')
    sys.exit(1)
# end if

if subprocess.call(['which', 'xgettext']) != 0:
    print('xgettext app not found')
    sys.exit(0)
# end if

if sys.argv[1] == 'extract':
    os.unlink(pot_path)
    for ( dirpath, dirnames, filenames ) in os.walk('ajenti', followlinks=True):
        if '/custom_' in dirpath:
            continue
        # end if
        if '/elements' in dirpath:
            continue
        # end if
        for f in filenames:
            path = os.path.join(dirpath, f)
            if f.endswith('.py'):
                print('Extracting from %s' % path)
                check_call([
                    'xgettext',
                    '-c',
                    '--from-code=utf-8',
                    '--omit-header',
                    '-o', pot_path,
                    '-j' if os.path.exists(pot_path) else '-dajenti',
                    path,
                ])
            # end if f.endswith('.py')
            if f.endswith('.xml'):
                print('Extracting from %s' % path)
                content = open(path).read()
                xml = etree.fromstring('<xml xmlns:bind="bind" xmlns:binder="binder">' + content + '</xml>')
                try:
                    msgs = []

                    def traverse(n):
                        for k, v in n.items():
                            if v.startswith('{') and v.endswith('}'):
                                msgs.append(v[1:-1])
                            try:
                                if "_('" in v:
                                    eval(v, {'_': msgs.append})
                            except:
                                pass
                            # end try
                        # next k, v
                        for c in n:
                            traverse(c)
                        # next c
                    traverse(xml)

                    fake_content = ''.join('gettext("%s");\n' % msg for msg in msgs)
                    fake_content = 'void main() { ' + fake_content + ' }'

                    open(path, 'w').write(fake_content)
                    check_call([
                        'xgettext',
                        '-C',
                        '--from-code=utf-8',
                        '--omit-header',
                        '-o', pot_path,
                        '-j' if os.path.exists(pot_path) else '-dajenti',
                        path,
                    ])
                finally:
                    open(path, 'w').write(content)
                # end try
            # end if f.endswith('.xml')
        # next f
    # next ( dirpath, dirnames, filenames )
# end if sys.argv[1] == 'extract'

if sys.argv[1] == 'compile':
    print( LANGUAGES )
    for lang in LANGUAGES:
        po_dir  = os.path.join( LOCALEDIR, lang, 'LC_MESSAGES' )
        po_path = os.path.join( po_dir, 'ajenti.po' )
        mo_path = os.path.join( po_dir, 'ajenti.mo' )

        if not os.path.exists( po_dir ):
            os.makedirs( po_dir )
        # end if

        print('Compiling %s' % lang)
        check_call([
            'msgfmt',
            po_path,
            '-v',
            '-o', mo_path
        ])
    # next lang
# end if sys.argv[1] == 'compile'