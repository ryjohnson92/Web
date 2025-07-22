import re,uuid,os
import sys, inspect
from flask import Flask
from functools import partial
from gunicorn.app.base import BaseApplication
from flask_restful import Resource,Api

class Register:
    def api_failure_wrap(func,*args,**kwargs):
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as err:
                print(err)
                return {}
        return wrapper

    class Resource(Resource):
        def __init__(self) -> None:
            super().__init__()
        pass
    def __init__(self,app) -> None:
        self.app = app
        print(self.__get_resources__())
    def __enter__(self):
        return self.app
    def __exit__(self,a,b,c):

        pass
    def __get_resources__(self)->list:
        t = []
        for x in dir(self):
            if not re.match(r'__.*__',x,flags=re.I) and str(x).lower() != 'resource':
                obj = getattr(self,x)
                if isinstance(obj, type):
                    route = getattr(obj,'ROUTE') if hasattr(obj,'ROUTE') else x.replace('_','/')
                    route = '/'+route
                    self.app.add_resource(obj,route)
                    print(route)
        pass
    pass

class FlaskGunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def debug(host:str,port:str,resources:list=[],flask_args:dict={"import_name":"app"},secret_key:str=str(uuid.uuid4())):
    app = Flask(**flask_args)
    app.config['SECRET_KEY']=secret_key
    api = Api(app)
    for _ in resources:
        with _(api): pass
    return (
        api,
        partial(app.run,debug=True,host=host,port=port)
    )

def prod(host:str,port:str,resources:list=[],flask_args:dict={"import_name":"app"},secret_key:str=str(uuid.uuid4())):
    app = Flask(**flask_args)
    app.config['SECRET_KEY']=secret_key
    api = Api(app)
    for _ in resources:
        with _(api): pass
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': int(os.environ.get('GUNICORN_WORKER_PROCS', '4')),
        'loglevel': 'info',
        'accesslog': '-',
        'errorlog': '-',
    }
    return (FlaskGunicornApp(app, options),FlaskGunicornApp(app, options).run)
