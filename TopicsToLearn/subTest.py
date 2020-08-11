import subprocess

## variable type definition
a : subprocess.CompletedProcess = subprocess.run(args=["ls", "-l:"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(a)