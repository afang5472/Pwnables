from pwn import *
import time

context.log_level = 'debug'
#init.
p = remote("pwnable.kr",9007)
p.recv()
time.sleep(3)
target = p.recvuntil("\n")
temp = target.split(" ")
N = temp[0].split("=")[1]
C = temp[1].split("=")[1]

def getres(payload):

    p.sendline(payload)
    res = p.recvuntil("\n")
    if "Correct" in res or "Wrong" in res:
        return "HIT"
    try:
        return int(res)
    except:
        return 9

def guess(A,B):

    t = ""
    for i in range(A,B):
        if i == B:
            t += str(i)
        else:
            t += str(i) + " "
    if t == "":
        t = str(A)
    res = getres(t)
    if res == "HIT":
        return "GOT"
    if res % 10 == 0:
        return 0
    else:
        return 1

counter = 0
def find(M,N):

    global counter
    if M == N or counter == 9:
        return (M, counter)
    if (M + N) %2 == 0:
        temp = (M+N)/2
    else:
        temp = (M+N+1)/2
    counter += 1
    reser = guess(M,temp)
    if reser == "GOT":
        counter = 10
        return (M,counter)
    if reser == 1:
        return find(M,temp)
    else:
        return find(temp,N)

target = find(0,int(N))
print target
M = target[0]
count = target[1]
if count == 10:
    Next = p.recv()
print "Let's start."
for i in range(10-count):
    p.sendline(str(M))
    re = p.recv(50)
    if "Correct" in re or "Wrong" in re:
        Next = p.recv()
        break
print Next
