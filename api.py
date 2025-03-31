import re,uuid
import sys, inspect
from flask import Flask
from functools import partial
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

def debug(host,port,flask_args:dict={"import_name":"app"},secret_key:str=str(uuid.uuid4())):
    app = Flask(**flask_args)
    app.config['SECRET_KEY']=secret_key
    api = Api(app)
    return (
        api,
        partial(app.run,debug=True,host=host,port=port)
    )