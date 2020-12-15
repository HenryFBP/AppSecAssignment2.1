import shlex, subprocess

evil_data='; wall "You have been hacked!"'

p = subprocess.Popen('ls', '-l', 'images/', evil_data) # popen defends against this

p.wait()

print("done")