#-------------------------------------------------------------------------------
# Copyright (c) 2010 M. George Hansen.
#
# optionparser is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# 
# optionparser is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# optionparser.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
"""
:Original Author: Russ Cox <rsc@plan9.bell-labs.com>
:Modified By: M. George Hansen <technopolitica@gmail.com>

Usage:
------
>>> import sys
>>> usagemessage=\
... '''usage: example.py [-h] [-f FILE] [-n N] [-q] who where
...     -h, --help                  show this help message
...     -f FILE, --file=FILE        write report to FILE
...     -n N, --num=N               print N copies of the report
...     -q, --quiet                 don't print status messages to stdout
... '''
>>> def main():
...     opt = OptionParser(usage=usagemessage)
...     report = 'default.file'
...     ncopies = 1
...     verbose = 1
...     for o in opt:
...         if o=='-f' or o=='--file':
...             report = opt.optarg()
...         elif o=='-n' or o=='--num':
...             ncopies = opt.optarg(opt.typecast(int, 'integer'))
...         elif o=='-q' or o=='--quiet':
...             verbose = 0
...         else:
...             opt.error('unknown option '+o)
...     if len(opt.args()) != 2:
...         opt.error('incorrect argument count')
...     print 'report=%s, ncopies=%s verbose=%s' % (report, ncopies, verbose)
...     print 'arguments: ', opt.args()
... 
"""
from __future__ import generators, print_function
import sys
import os.path
import re

class OptionError(Exception):
    pass

class OptionParser:
    short_option_re = re.compile(r'^\s*-([A-Za-z]+)\s*$')
    long_option_re = re.compile(
        r'^\s*(--[A-Za-z][A-Za-z-]+)(?:\s*|=([^\s]*)\s*)$'
    )
    
    def __init__(self, args=None, prog=None, usage='', version=''):
        if (prog is None):
            self.prog = os.path.basename(sys.argv[0])
        else:
            self.prog = prog
        if (args is None):
            self.args = sys.argv[1:]
        else:
            self.args = args
        self.usage = usage.format(prog=self.prog)
        self.version = '{prog} version {version}'.format(prog=self.prog,
                                                         version=version)
        self.current_option = None
    
    def __iter__(self):
        program_arguments = []
        while len(self.args) > 0:
            arg = self.args.pop(0)
            if (self.short_option_re.match(arg)):
                # next token is one or more short options
                match = self.short_option_re.match(arg)
                options = ['-{0}'.format(abv) for abv in match.group(1)]
                for opt in options:
                    self.current_option = opt
                    yield opt
            elif (self.long_option_re.match(arg)):
                # next token is a long option that may have its argument
                # attached
                match = self.long_option_re.match(arg)
                option = match.group(1)
                self.current_option = option
                attached_arg = match.group(2)
                if (attached_arg is not None):
                    self.args.insert(0, attached_arg)
                yield option
            else:
                program_arguments.append(arg)
        self.current_option = None
        self.args = program_arguments
        while True:
            raise StopIteration
    
    def get_next_option_arg(self, type_=str):
        if (self.current_option is not None):
            try:
                arg = self.args.pop(0)
            except IndexError:
                arg = None
            if (arg is None or self.short_option_re.match(arg) or
                self.long_option_re.match(arg)):
                message = '{0} option expected a {1} argument but got nothing'
                message = message.format(
                    self.current_option,
                    getattr(type_, '__name__', type_)
                )
                self.error(message)
        else:
            message = 'no option is currently being parsed'
            raise OptionError(message)
        
        try:
            result = type_(arg)
        except ValueError:
            message = '''{0} expected a {1} argument but was unable to type
cast "{2}"'''
            message = message.format(
                self.current_option,
                getattr(type_, '__name__', type_),
                arg
            )
            self.error(message)
        return result
    
    def get_next_prog_arg(self, type_=str):
        try:
            arg = self.args.pop(0)
        except IndexError:
            arg = None
        if (arg is None or self.short_option_re.match(arg) or
            self.long_option_re.match(arg)):
            message = 'expected a {0} argument but got nothing'
            message = message.format(getattr(type_, '__name__', type_))
            raise OptionError(message)
        try:
            result = type_(arg)
        except ValueError:
            message = '''{0} expected a {1} argument but was unable to type
cast "{2}"'''
            message = message.format(
                self.current_option,
                getattr(type_, '__name__', type_),
                arg
            )
            self.error(message)
        return result
    
    def error(self, message):
        if (self.usage is not None):
            print('option error: {0}\n\n{1}'.format(message, self.usage),
                  file=sys.stderr)
            sys.exit(0)
        else:
            raise OptionError(message)
