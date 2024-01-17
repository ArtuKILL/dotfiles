import re
import subprocess
from multiprocessing import Process
import json

cmd = ['ping', '-c 1', '8.8.8.8']

js = {
    "text": "error",
    "percentage": 100,
    "code": -1
    # "class": ""
}


def ping(js):
    ping = None
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    pattern = r"rtt min/avg/max/mdev = ([0-9.]+)/([0-9.]+)/([0-9.]+)/([0-9.]+) ms"
    match = re.search(pattern, result)

    if match:
        ping = match.group(1)
        js["text"] = ping
        ping = float(ping)

    if type(ping) is not float:
        print(json.dumps(js))
        return

    js["text"] = str(round(float(ping), 2))

    if ping <= 100:
        js["percentage"] = 0

    if ping > 100:
        js["percentage"] = 25

    if ping > 300:
        js["percentage"] = 50

    print(json.dumps(js))


ping_process = Process(target=ping, name="ping", args=(js,))
ping_process.start()
ping_process.join(timeout=6)
ping_process.terminate()
code = ping_process.exitcode
js["code"] = code


if bool(code) != bool(code != 0):
    print(json.dumps(js))
print(js)
