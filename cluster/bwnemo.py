#! /usr/bin/env python

"""This module provides the handler for the BWNemo cluster

"""
from __future__ import division, print_function

import datetime
import os
import subprocess
import time

import yaml

import utils

stub = """#!/usr/bin/env bash

#MSUB -l nodes={nnodes}:ppn={nprocs}
#MSUB -l walltime={walltime}

python execute_taskfile.py {joblistfile} &&

/usr/bin/mv {joblistfile}* {donejobfolder}
"""

PENDINGJOBFOLDER = 'jobs/pending/'
utils.ensure_exist(PENDINGJOBFOLDER)
RUNNINGJOBFOLDER = 'jobs/running/'
utils.ensure_exist(RUNNINGJOBFOLDER)
DONEJOBFOLDER    = 'jobs/done/'
utils.ensure_exist(DONEJOBFOLDER)
TASKFILES        = 'jobs/tasks/'
utils.ensure_exist(TASKFILES)
JOBLISTFILE      = 'jobs/jobs'
utils._touch(JOBLISTFILE)


def execute(jobs, timeperjob, nnodes, nprocs, walltime):
    unique_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    njobs = int(walltime / timeperjob) * nprocs * nnodes
    joblistfiles = utils.get_joblistfiles(TASKFILES + unique_name, jobs, njobs)

    taskfiles = []
    for i, joblistfile in enumerate(joblistfiles):
        taskfiles.append(PENDINGJOBFOLDER + unique_name + '_{:03d}'.format(i))
        with open(taskfiles[-1], 'w') as f:
            content = stub.format(nnodes=nnodes, nprocs=nprocs,
                                  walltime=walltime, joblistfile=joblistfile,
                                  donejobfolder=DONEJOBFOLDER)
            f.write(content)
    print(taskfiles)

    # ensure that the filesystem is up to date
    time.sleep(.1)

    for i, taskfile in enumerate(taskfiles):
        try:
            jobid = subprocess.check_output(['msub', taskfile])
        except subprocess.CalledProcessError:
            raise
        # with utils.LockedFile(JOBLISTFILE, 'r+') as f:
        with open(JOBLISTFILE, 'r+') as f:
            data = yaml.load(f.read())
            if data is None:
                data = []
            data.append({jobid: joblistfiles[i]})
            f.seek(0)
            f.write(yaml.dump(data))