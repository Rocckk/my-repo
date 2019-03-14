import subprocess as sh




r = sh.run('ls ~', shell=True, stdout=sh.PIPE)

print(r.returncode)
print(r.stdout.decode())
print(type(r.stdout))


