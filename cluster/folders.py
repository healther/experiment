import os

import utils


LOCATION         = os.path.split(os.path.realpath(__file__))[0]
PENDINGJOBFOLDER = os.path.join(LOCATION, 'jobs/pending/')
utils.ensure_exist(PENDINGJOBFOLDER)
RUNNINGJOBFOLDER = os.path.join(LOCATION, 'jobs/running/')
utils.ensure_exist(RUNNINGJOBFOLDER)
DONEJOBFOLDER    = os.path.join(LOCATION, 'jobs/done/')
utils.ensure_exist(DONEJOBFOLDER)
TASKFILEFOLDER   = os.path.join(LOCATION, 'jobs/tasks/')
utils.ensure_exist(TASKFILEFOLDER)
JOBLISTFILE      = os.path.join(LOCATION, 'jobs/jobs')
utils._touch(JOBLISTFILE)
