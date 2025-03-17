import json
from gunicorn_conf import *

reload = True

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
    "reload": reload,
}


print(json.dumps(log_data))
