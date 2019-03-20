import subprocess as sub

proc = sub.run('zcat', shell=True, timeout=5)

print(proc)
