import subprocess as sh



try:
    r = sh.run('sh', shell=True, stdout=sh.PIPE, stderr = sh.STDOUT, timeout=3)

    print(r.returncode)      



except sh.TimeoutExpired:
    r = sh.run('cat test_file.txt', shell=True, stdout=sh.PIPE, stderr = sh.STDOUT, timeout=3)
    print(r.returncode)
    print(r.stdout)
     

