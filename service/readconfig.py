def readConfig():
    import inspect
    import os
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))
    configPath = os.path.join(dirpath, 'config.ini')
    fconfig = open(configPath, 'r')
    username = fconfig.readline()
    username = username[username.find(':')+1:username.find(';')]
    password = fconfig.readline()
    password = password[password.find(':')+1:password.find(';')]
    circle = fconfig.readline()
    circle = circle[circle.find(':')+1:circle.find(';')]
    return [username, password, circle]
