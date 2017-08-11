import os
import sys
import time
import getpass
import platform
import datetime
from os.path import expanduser

def get_output_dir(params):
    venvpath, testfilepath = params
    old_os_path = os.environ['PATH']
    old_sys_path = list(sys.path)
    old_sys_prefix = sys.prefix
    basename = "mylogfile"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix]) # e.g. 'mylogfile_120508_171442'
    venvpath_mod =  os.path.split(venvpath)[0]
    filepath = os.path.join(venvpath_mod, filename)
    
    testsuite = testfilepath.split(".")[0]
    outputdir = os.path.join(os.path.expanduser('~'),testsuite+time.strftime("%Y%m%d_%H%M%S"))

    with open(filepath,'w') as fp:
        pass
    activate_this =  os.path.join(venvpath, 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))
    print testfilepath, outputdir, filepath
    print 'above are the path'
    print "************************************"
    os.system('sutas -s '+ testfilepath + ' -c dsad -logpath ' + outputdir + ' > ' + filepath)
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    print(filename)
    os.environ['PATH'] = old_os_path
    sys.prefix = old_sys_prefix
    sys.path[:0] = old_sys_path
    return outputdir

def get_free_envs():
    free_env = []
    if platform.system() == 'Windows':
        envhome = os.path.join(expanduser('~'), 'Envs')
    else:
	envhome = os.path.dirname(os.path.abspath(__file__)).split('NUTAS',1)[0] +  '.virtualenvs'
    print("Environment home: " + envhome)
    
    envs = os.listdir(envhome)
    for env in envs:
        lockfilepath =  os.path.join(envhome, env, 'sutaslock.txt')
        if not os.path.isfile(lockfilepath):
            if platform.system() == 'Windows':
                venvpath = os.path.join(envhome, env, 'Scripts')
                free_env.append(venvpath)
            else:
                venvpath = os.path.join(envhome, env, 'bin')
                if os.path.isdir(venvpath): 
                    free_env.append(venvpath)
    
    return free_env
