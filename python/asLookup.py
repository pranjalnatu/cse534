import subprocess

# test echo
a = subprocess.call(["echo", 'hello world'])
b = subprocess.call(["echo" ,'hello world'])


# Compose a query to haseeb's AS lookup service
# echo "[command]" | netcat as.haseebniaz.com 22
# -info	Get info about an AS, IP or IP prefix
# 				-> echo "-info ASNUM"


ncat = ' | netcat as.haseebniaz.com 22'


blah = subprocess.call(["echo", "-info AS1234", "|", "netcat", "as.haseebniaz.com", "22"])