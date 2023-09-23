import pytest
from sshcheckers import ssh_checkout
import random
import string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(f"mkdir {data['ip']} {data['user']} {data['passwd']} {data['folderin']} {data['folderout']}", "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(f"rm -rf {data['ip']}/* {data['user']}/* {data['passwd']}/* {data['folderin']}/* {data['folderout']}/*", "")


@pytest.fixture()
def make_files(data):
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f"cd {data['folderin']}; dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock", data['ip'], data['user'], data['passwd']):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder(data):
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(f"cd {data['folderin']}; mkdir {subfoldername}", data['ip'], data['user'], data['passwd']):
        return None, None
    if not ssh_checkout(f"cd {data['folderin']}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock", data['ip'], data['user'], data['passwd']):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f"Start: {datetime.now().strftime('%H:%M:%S.%f')}")
    yield
    print(f"Finish: {datetime.now().strftime('%H:%M:%S.%f')}")
    with open("stat.txt", "a") as stat_file:
        stat_file.write(f"{datetime.now().strftime('%H:%M:%S.%f')}, {data['count']}, {data['bs']}, {open('/proc/loadavg').read()}")

@pytest.fixture()
def start_time():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")