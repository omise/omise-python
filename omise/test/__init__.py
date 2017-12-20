import sys

try:
    basestring
except NameError:
    basestring = str

if sys.version_info[0] == 2:
    def next(o, **kw):
        return o.next(**kw)
