#! /usr/bin/env python

import datetime
import multiprocessing as mp
import os
import shutil
import subprocess
import sys

import utils


location=os.path.split(os.path.realpath(__file__))[0]
PENDINGFOLDER = os.path.join(location, 'jobs/pending/')
RUNNINGJOBFOLDER = os.path.join(location, 'jobs/running/')
DONEJOBFOLDER = os.path.join(location, 'jobs/done/')
TASKFILES        = os.path.join(location, 'jobs/tasks/')


def execute_jobfile(jobfile):
    utils._touch(jobfile + '.start')
    try:
        stdoutfile = open(jobfile + 'out', 'w')
        ret_value = subprocess.call(['bash', jobfile],
                                     cwd=os.path.dirname(jobfile),
                                     stdout=stdoutfile)
        utils._touch(jobfile + '.finish')
        if ret_value == 0:
            utils._touch(jobfile + '.success')
    except Exception as e:
        # FIXME: Improve error handling
        print("{} found exception {}".format(datetime.datetime.now(), e))
        utils._touch(jobfile + '.finish')


# read file with the task scripts
taskfile = sys.argv[1]
shutil.move(os.path.join(PENDINGFOLDER, taskfile), RUNNINGJOBFOLDER)
with open(os.path.join(TASKFILES, taskfile), 'r') as f:
    jobfiles = [line.strip() for line in f]

nproc = int(os.getenv('MOAB_PROCCOUNT', '1'))
if nproc > 1:
    pool = mp.Pool(nproc)
    pool.map(execute_jobfile, jobfiles)
    pool.close()
    pool.join()
else:
    for jobfile in jobfiles:
        execute_jobfile(jobfile)

shutil.move(os.path.join(RUNNINGJOBFOLDER, taskfile), DONEJOBFOLDER)
