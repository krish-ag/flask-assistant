from werkzeug.local import LocalStack

class Context(dict):
    """docstring for _Context"""
    def __init__(self, name, parameters={}, lifespan=5):

        self.name = name
        self.parameters = parameters
        self.lifespan = lifespan

    def __setitem__(self, param, val):
        self.parameters[param] = val

    def __getitem__(self, param):
        if param in 'nameparameterslifespan':
            return super().__getitem__(param)
        return self.parameters[param]

    # def __setattr__(self, param, val):
    #     self.parameters[param] = val

    # def __getattr__(self, param):
    #     if param not in 'namelifespanparameters':
    #         return self.parameters[param]

    # def __getitem__(self, param):


    def set(self, param_name, value):
        self.parameters[param_name] = value

    def get(self, param):
        return self.parameters[param]

    def sync(self, context_json):
        self.__dict__.update(context_json)

    def __repr__(self):
        return self.name


    @property
    def serialize(self):
        return {"name": self.name, "lifespan": self.lifespan, "parameters": self.parameters}
    
class ContextManager():

    def __init__(self):
        self._cache = {}

    # def __getattr__(self, attr):
#         # converts timestamp str to datetime.datetime object
#         if 'timestamp' in attr:
#             return aniso8601.parse_datetime(self.get(attr))
#         return self.get(attr)

#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)


    def add(self, *args, **kwargs):
        context = Context(*args, **kwargs)
        self._cache[context.name] = context
        return context

    def get(self, context_name):
        return self._cache.get(context_name, Context(context_name))

    def set(self, context_name, param, val):
        context = self.get(context_name)
        context.set(param, val)
        return context


    def get_param(self, context, param):
        return self._cache

    def update(self, contexts_json):
        for obj in contexts_json:
            context = self.get(obj['name'])
            context.lifespan = obj['lifespan']
            context.parameters = obj['parameters']
            self._cache[context.name] = context


    @property
    def status(self):
        return {
            'Active contexts': self.active,
            'Expired contexts': self.expired,
        }


    @property
    def active(self):
        return [self._cache[c] for c in self._cache if self._cache[c].lifespan > 0]

    @property
    def expired(self):
        return [self._cache[c] for c in self._cache if self._cache[c].lifespan == 0]
    



    

