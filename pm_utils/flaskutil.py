from warnings import warn

from werkzeug.datastructures import ImmutableMultiDict


class dictobj(dict):
    """ a dict-like object:
    * whose values can also be get/set using the `obj.key` notation
    * object[key] returns None if the key is not known
    """

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __getitem__(self, name):
        if name in self:
            return super(dictobj, self).__getitem__(name)
        return None

    def copy(self):
        return self.__class__((k, self[k]) for k in self)


class argsdict(dictobj):
    types = {}
    defaults = {}

    def __init__(self, reqargs=None, defaults=None, types=None):
        """ transforms the request args (or any such dict) for convenience :
        * be a malleable dictobj (whose missing attrs/keys default to None)
        * set the default values (if any, defaults is a mapping from keys
          to a scalar or a collable)
        * coerce to the wanted types (if any, types is a mapping from keys
          to a type or factory function)
        """
        super(argsdict, self).__init__()
        if reqargs is None:  # copy constructor
            return

        defaults = defaults or self.defaults
        if not isinstance(reqargs, ImmutableMultiDict):
            for k, v in reqargs.items():
                self[k] = v
            self._set_defaults(defaults)
            return

        types = types or self.types
        self._set_types(reqargs.to_dict(flat=False), defaults, types)

    def _set_types(self, args, defaults, types):
        for key, val in args.items():
            # when sending json, attributes land as `<attribute>[]`
            islist = key.endswith('[]')
            key = key.rstrip('[]')
            targettype = types.get(key)
            # signal if there is any discrepancy and force to tuple
            if islist and targettype not in (list, tuple):
                warn('element %r is a sequence but its expected type is %r' %
                     (key, targettype))
                targettype = tuple
            # val can be an str or a sequence of strs
            # hence `not filter(None, val)` gets us all
            # the falsy values ('', [''])
            if not list(filter(None, val)):
                # no value -> default value
                default = defaults.get(key)
                self[key] = default() if callable(default) else default
            else:
                self[key] = val if targettype in (list, tuple) else val[0]
            # type coercion
            if targettype:
                self[key] = targettype(self[key])
        self._set_defaults(defaults)

    def _set_defaults(self, defaults=None):
        defaults = defaults or self.defaults
        # complete entries with mandatory defaults
        for key, val in defaults.items():
            if key not in self:
                self[key] = val() if callable(val) else val

    def copy(self):
        new = self.__class__()
        for k in self:
            new[k] = self[k]
        return new


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
