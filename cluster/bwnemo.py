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

python {location}/execute_taskfile.py {joblistfile}
"""

location=os.path.split(os.path.realpath(__file__))[0]
PENDINGJOBFOLDER = os.path.join(location, 'jobs/pending/')
utils.ensure_exist(PENDINGJOBFOLDER)
RUNNINGJOBFOLDER = os.path.join(location, 'jobs/running/')
utils.ensure_exist(RUNNINGJOBFOLDER)
DONEJOBFOLDER    = os.path.join(location, 'jobs/done/')
utils.ensure_exist(DONEJOBFOLDER)
TASKFILES        = os.path.join(location, 'jobs/tasks/')
utils.ensure_exist(TASKFILES)
JOBLISTFILE      = os.path.join(location, 'jobs/jobs')
utils._touch(JOBLISTFILE)


def execute(jobs, timeperjob, nnodes, nprocs, walltime):
    unique_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    njobs = int(walltime / timeperjob) * nprocs * nnodes
    joblistfiles = utils.get_joblistfiles(TASKFILES + unique_name, jobs, njobs)

    taskfiles = []
    for i, joblistfile in enumerate(joblistfiles):
        taskfiles.append(unique_name + '_{:03d}'.format(i))
        with open(os.path.join(PENDINGJOBFOLDER, taskfiles[-1]), 'w') as f:
            content = stub.format(nnodes=nnodes, nprocs=nprocs,
                                  walltime=walltime, joblistfile=joblistfile,
                                  donejobfolder=DONEJOBFOLDER,
                                  location=location)
            f.write(content)
    # ensure that the filesystem is up to date
    time.sleep(.1)

    for i, taskfile in enumerate(taskfiles):
        try:
            jobid = subprocess.check_output(['msub', os.path.join(PENDINGJOBFOLDER, taskfile)])
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
