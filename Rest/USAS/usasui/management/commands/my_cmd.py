
from django.core.management.base import BaseCommand, CommandError
from usasui.models import TestRequest
from usasui.utils import get_output_dir, get_free_envs
from multiprocessing import Pool
import subprocess
import os
import platform
import logging
import sys
import datetime
from os.path import expanduser
from robot.api import ExecutionResult, ResultVisitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'My custom django management command'

    # def get_output_dir(self,venvpath=None, testfilepath=None):
    #     old_os_path = os.environ['PATH']
    #     old_sys_path = list(sys.path)
    #     old_sys_prefix = sys.prefix
    #     basename = "mylogfile"
    #     suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '.txt'
    #     filename = "_".join([basename, suffix]) # e.g. 'mylogfile_120508_171442'
    #     venvpath_mod =  os.path.split(venvpath)[0]
    #     filepath = os.path.join(venvpath_mod, filename)
    #     with open(filepath,'w') as fp:
    #         pass
    #     activate_this =  os.path.join(venvpath, 'activate_this.py')
    #     execfile(activate_this, dict(__file__=activate_this))
    #     #subprocess.call(['sutas', '-s', 'C:\\Users\\nexii\\xyz.txt', '-c', 'dsad'])
    #     os.system('sutas -s '+ testfilepath + ' -c dsad > ' + filepath)
    #     print(filename)
    #     os.environ['PATH'] = old_os_path
    #     sys.prefix = old_sys_prefix
    #     sys.path[:0] = old_sys_path
    #     return filepath

    def get_free_envs(self):
        free_env = []
        if platform.system() == 'Windows':
            envhome = os.path.join(expanduser('~'), 'Envs')
        else:
            envhome = os.path.join(expanduser('~'), '.virtualenvs')
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


    def handle(self, *args, **options):
        # status = options['test'][0]
        status = "W"
        # Printing all related Testcase(T,W,C,E):
        print "Your Test for ",status + " are as ...."
        test_qs = TestRequest.objects.filter(status=status)
        test_qs = [obj for obj in test_qs]
        free_envs = get_free_envs()
        results = {}
        pool = Pool(len(free_envs))
        for i,env in enumerate(free_envs):
            try:
                first_arg = env
                second_arg = test_qs[i].test_file.file.name
                obj = test_qs[i]
                obj.status = TestRequest.TESTING
                obj.envt = env.split('/')[::-1][1]
                obj.save()
                logger.info('Running test using virtualenv ' + env)
                print("Using following env for test execution:" + env)
                result = pool.apply_async(get_output_dir, [(first_arg, second_arg)])
                results[obj.id] = result
            except Exception as e:
                print("Some exception has happened")
                print(e)
                break;

        for k,res in results.items():
            try:
                test = TestRequest.objects.get(id=k)
                test.log_path = '/media/' + res.get().split('/')[::-1][0]+'/log.html'
                xml_path = os.path.dirname(os.path.abspath(__file__)).split('NUTAS',1)[0] + 'NUTAS/UI/USAS/media/' + res.get().split('/')[::-1][0]+'/output.xml'
                test.status = TestRequest.COMPLETED
                result = ExecutionResult(xml_path)
                stats = result.statistics
                if stats.total.critical.failed:
                    test.result = 'Failed'
                else:
                    test.result = 'Passed'            
                test.save()
            except Exception as e:
                print('exception from management command')
                print(e)

