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
from folders import PENDINGJOBFOLDER, DONEJOBFOLDER, TASKFILEFOLDER, \
                    JOBLISTFILE, LOCATION

stub = """#!/usr/bin/env bash

#MSUB -l nodes={nnodes}:ppn={nprocs}
#MSUB -l walltime={walltime}

python {location}/execute_taskfile.py {joblistfile}
"""


def execute(jobs, timeperjob, nnodes, nprocs, walltime):
    unique_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    njobs = int(walltime / timeperjob) * nprocs * nnodes
    joblistfiles = utils.get_joblistfiles(TASKFILEFOLDER + unique_name,
                                          jobs, njobs)

    taskfiles = []
    for i, joblistfile in enumerate(joblistfiles):
        taskfiles.append(unique_name + '_{:03d}'.format(i))
        with open(os.path.join(PENDINGJOBFOLDER, taskfiles[-1]), 'w') as f:
            content = stub.format(nnodes=nnodes, nprocs=nprocs,
                                  walltime=walltime, joblistfile=joblistfile,
                                  donejobfolder=DONEJOBFOLDER,
                                  location=LOCATION)
            f.write(content)
    # ensure that the filesystem is up to date
    time.sleep(.1)

    for i, taskfile in enumerate(taskfiles):
        try:
            jobid = subprocess.check_output(['msub',
                                    os.path.join(PENDINGJOBFOLDER, taskfile)])
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
