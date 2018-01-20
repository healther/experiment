#! /usr/bin/env python

"""This module provides the handler for the hel cluster

"""
from __future__ import division, print_function

import datetime
import os
import subprocess
import time

import json

from . import utils
from .utils import PENDINGJOBFOLDER, TASKFILEFOLDER, JOBLISTFILE, LOCATION

stub = """#!/usr/bin/env bash
export MYSECRETVAR_NPROC=$SLURM_JOB_CPUS_PER_NODE

python {location}/execute_taskfile.py {joblistfile}
"""


def execute(jobs, timeperjob, nprocs, walltime, queue):
    unique_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    njobs = int(walltime / timeperjob) * nprocs
    taskfiles = utils.get_joblistfiles(unique_name,
                                          jobs, njobs)

    for i, taskfile in enumerate(taskfiles):
        with open(os.path.join(PENDINGJOBFOLDER, taskfile), 'w') as f:
            content = stub.format(
                            joblistfile=os.path.join(TASKFILEFOLDER, taskfile),
                            location=LOCATION)
            f.write(content)
    # ensure that the filesystem is up to date
    time.sleep(.1)

    for i, taskfile in enumerate(taskfiles):
        try:
            jobid = subprocess.check_output(['sbatch',
                                '-c', '{}'.format(nprocs),
                                '-p', '{}'.format(queue),
                                '--wrap=bash {}'.format(
                                    os.path.join(PENDINGJOBFOLDER, taskfile))])
            jobid = jobid.strip().split()[-1]
        except subprocess.CalledProcessError:
            raise
        # with utils.LockedFile(JOBLISTFILE, 'r+') as f:
        with open(JOBLISTFILE, 'r') as f:
            data = json.load(f)
        if data is None:
            data = []
        data.append({jobid: os.path.join(TASKFILEFOLDER, taskfiles[i])})
        with open(JOBLISTFILE, 'w') as f:
            json.dump(data, f)
