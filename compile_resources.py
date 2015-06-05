#!/usr/bin/env python
# coding=utf-8
# ---------------------------------------------------------------------------
# Resource compiler for Ajenti plugins.
#
#   Copyright (C) 2015 Marc Bertens <m.bertens@pe2mbs.nl>
#   Adapted from compile_resources.py by Eugene Pankov
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
import subprocess
import shutil
import glob
import os
import re
import sys
import gevent

try:
    from gevent import subprocess
except:
    import subprocess

import uuid
import threading

def check_output(*args, **kwargs):
    try:
        return subprocess.check_output(*args, **kwargs)
    except Exception as e:
        print( 'Call failed' )
        print( ' '.join( args[ 0 ] ) )
        print( str( e ) )
        sys.exit( 0 )
    # end try
    return
# end def

def dirname():
    return 'tmp/' + str(uuid.uuid4())

def compile_coffeescript( inpath ):
    outpath = '%s.c.js' % inpath

    if os.path.exists(outpath) and os.stat(outpath).st_mtime > os.stat(inpath).st_mtime:
        print('Skipping %s' % inpath)
        return
    # end if
    print( 'Compiling CoffeeScript: %s' % inpath )

    d = dirname()
    check_output( 'coffee -o %s -c "%s"' % (d, inpath), shell=True )
    shutil.move( glob.glob('./%s/*.js' % d)[0], outpath)
    shutil.rmtree( d )
    return
# end def

def compile_less( inpath ):
    outpath = '%s.c.css' % inpath

    if os.path.exists(outpath) and os.stat(outpath).st_mtime > os.stat(inpath).st_mtime:
        print('Skipping %s' % inpath)
        #return
    # end if
    print('Compiling LESS %s' % inpath)
    out = check_output('lessc "%s" "%s"' % (inpath, outpath), shell=True)
    if out:
        print( "ERROR: %s" % ( out ) )
    #print subprocess.check_output('recess --compile "%s" > "%s"' % (inpath, outpath), shell=True)
    return
# end def

compilers = {
    r'.+\.coffee$': compile_coffeescript,
    r'.+[^i]\.less$': compile_less,
}

greenlets = []

def traverse( fx ):
    plugins_path = '.'
    path = os.path.join( plugins_path, 'layout' )
    print( path )
    if os.path.exists( path ):
        print( 'exists' )
        for (dp, dn, fn) in os.walk( path ):
            print( dp, dn, fn )
            for name in fn:
                file_path = os.path.join( dp, name )
                print( file_path )
                greenlets.append( gevent.spawn( fx, file_path ) )
            # next
        # next
    # end if
    done = 0
    done_gls = []
    length = 40
    total = len( greenlets )
    print

    while True:
        for gl in greenlets:
            print( gl )
            if gl.ready() and not gl in done_gls:
                done_gls.append( gl )
                done += 1
                dots = int(1.0 * length * done / total)
                sys.stdout.write('\r%3i/%3i [' % (done, total) + '.' * dots + ' ' * (length - dots) + ']')
                sys.stdout.flush()
            # end if
        # next
        gevent.sleep( 0.1 )
        if done == total:
            print
            break
        # end if
    # end while
    return
# end def

def compile( file_path ):
    for pattern in compilers:
        if re.match( pattern, file_path ):
            compilers[ pattern ]( file_path )
        # end if
    # next
# end def

if not os.path.exists('tmp'):
    os.mkdir('tmp')
# end if
greenlets = []
traverse( compile )
