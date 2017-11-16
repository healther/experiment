#! /usr/bin/env python

import datetime
import multiprocessing as mp
import os
import shutil
import subprocess
import sys

import utils


location=os.path.split(os.path.realpath(__file__))[0]
RUNNINGJOBFOLDER = os.path.join(location, 'jobs/running/')
DONEJOBFOLDER = os.path.join(location, 'jobs/done/')


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
shutil.move(taskfile, RUNNINGJOBFOLDER)
taskfile = os.path.join(RUNNINGJOBFOLDER, os.path.basename(taskfile))
with open(taskfile, 'r') as f:
    jobfiles = [line.strip() for line in f]

nproc = int(os.getenv('SLURM_CPUS_ON_NODE', '1'))
pool = mp.Pool(nproc)
pool.map(execute_jobfile, jobfiles)
pool.close()
pool.join()

shutil.move(taskfile, DONEJOBFOLDER)
