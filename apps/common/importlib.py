from django.utils.importlib import import_module
from django.core import exceptions

def load_class_from_path(path):
    try:    
        mw_module, mw_classname = path.rsplit('.', 1)
    except ValueError, e:
        raise exceptions.ImproperlyConfigured("Unable to parse class path '%s'" % path)
    try:
        mod = import_module(mw_module)
    except ImportError, e:
        raise exceptions.ImproperlyConfigured('Error importing module %s: "%s"' % (mw_module, e))
    try:
        mw_class = getattr(mod, mw_classname)
    except AttributeError:
        raise exceptions.ImproperlyConfigured('Module "%s" does not define a "%s" class' % (mw_module, mw_classname))
    mw_instance = mw_class()
    return mw_instance