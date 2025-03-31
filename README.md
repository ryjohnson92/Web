# Web
Useful web assets

## Register

```python
import os
from Web.api import Register,debug

class Example(Register):
    class search(Register.Resource):
        ROUTE ='api/search'
        def get(self):
            return 'HI'

if __name__ == "__main__":
    resources = [
        Example
    ]
    api,run = debug(host='0.0.0.0',port="8080",flask_args={
        "import_name":"app",
        "template_folder":'{}'.format(os.getcwd())
    },resources=resources)

    run()
```