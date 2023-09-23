from main import getout
from sshcheckers import ssh_checkout, upload_files,  ssh_getout
import pytest
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestPositive:


   def save_log(self, starttime, name):
       with open(name, 'w') as f:
           f.write(getout("journalctl --since '{}'".format(starttime)))


   def test_step1(self, start_time):
       res = []
       upload_files(data["ip"], data["user"], data["passwd"], data["pkgname"]+".deb",
                    "/home/{}/{}.deb".format(data["user"], data["pkgname"]))
       res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -i"
               " /home/{}/{}.deb".format(data["passwd"], data["user"], data["pkgname"]),
                               "Настраивается пакет"))
       res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "echo '{}' | "
                   "sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]),
                               "Status: install ok installed"))
       self.save_log(start_time, "log1.txt")
       assert all(res), "test1 FAIL"


   def test_step2(self, make_folders, clear_folders, make_files, start_time):
       res1 = ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {};"
           " 7z a {}/arx2".format(data["folderin"], data["folderout"]), "Everything is Ok")
       res2 = ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folderout"]), "arx2.7z")
       self.save_log(start_time, "log2.txt")
       assert res1 and res2, "test2 FAIL"


   def test_step3(self, clear_folders, make_files, start_time):
       res = []
       res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a "
           "{}/arx2".format(data["folderin"], data["folderout"]), "Everything is Ok"))
       res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z e "
           "arx2.7z -o{} -y".format(data["folderout"], data["folder_ext"]), "Everything is Ok"))
       for item in make_files:
           res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext"]), item))
       self.save_log(start_time, "log3.txt")
       assert all(res), "test3 FAIL"


   def test_step4(self, start_time):
       self.save_log(start_time, "log4.txt")
       assert ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z t"
           " arx2.7z".format(data["folderout"]), "Everything is Ok"), "test4 FAIL"


   def test_step5(self, start_time):
       self.save_log(start_time, "log5.txt")
       assert ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z u"
           " arx2.7z".format(data["folderin"]), "Everything is Ok"), "test5 FAIL"
