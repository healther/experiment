#! /usr/bin/env python

import datetime
import multiprocessing as mp
import os
import shutil
import subprocess
import sys

if 1: #__package__ is None:
    sys.path.insert(0, os.path.dirname( os.path.abspath(__file__) ) )
    import utils
    from utils import PENDINGJOBFOLDER, RUNNINGJOBFOLDER, DONEJOBFOLDER, \
                        TASKFILEFOLDER
else:
    from . import utils
    from .utils import PENDINGJOBFOLDER, RUNNINGJOBFOLDER, DONEJOBFOLDER, \
                        TASKFILEFOLDER



def execute_jobfile(jobfile):
    utils._touch(jobfile + '.start')
    try:
        stdoutfile = open(jobfile + 'out', 'w')
        stderrfile = open(jobfile + 'err', 'w')
        ret_value = subprocess.call(['bash', jobfile],
                                     cwd=os.path.dirname(jobfile),
                                     stdout=stdoutfile,
                                     stderr=stderrfile)
        utils._touch(jobfile + '.finish')
        if ret_value == 0:
            utils._touch(jobfile + '.success')
    except Exception as e:
        # FIXME: Improve error handling
        print("{} found exception {}".format(datetime.datetime.now(), e))
        utils._touch(jobfile + '.finish')


# read file with the task scripts
taskfile = os.path.basename(sys.argv[1])
shutil.move(os.path.join(PENDINGJOBFOLDER, taskfile), RUNNINGJOBFOLDER)
with open(os.path.join(TASKFILEFOLDER, taskfile), 'r') as f:
    jobfiles = [line.strip() for line in f]

nprocstr = os.getenv('MYSECRETVAR_NPROC', '1')
try:
    nproc = int(nprocstr) if nprocstr != '' else 1
except:
    nproc = 1

if nproc > 1:
    pool = mp.Pool(nproc)
    pool.map(execute_jobfile, jobfiles)
    pool.close()
    pool.join()
else:
    for jobfile in jobfiles:
        execute_jobfile(jobfile)

shutil.move(os.path.join(RUNNINGJOBFOLDER, taskfile), DONEJOBFOLDER)
