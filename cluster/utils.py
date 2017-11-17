import os
import time


class TimeOutError(Exception):
    pass


class LockedFile(object):
    """docstring for LockedFile"""
    def __init__(self, locked_file, mode, timeout=60.):
        super(LockedFile, self).__init__()
        self.locked_file = locked_file
        self.mode = mode
        self.timeout = timeout

    def __enter__(self):
        nrepeat = int(self.timeout / 1.)
        for _ in range(nrepeat):
            if not os.path.exists(self.locked_file + '.lock'):
                _touch(self.locked_file + '.lock')
                if not os.path.exists(self.locked_file):
                    _touch(self.locked_file)
                self.open_file = open(self.locked_file, self.mode)
            else:
                time.sleep(1.)
        else:
            raise TimeOutError("Timed out trying to acquire lock for {}"
                               "".format(self.locked_file))

    def __exit__(self):
        self.open_file.close()
        os.remove(self.locked_file + '.lock')


def ensure_exist(folder):
    try:
        os.makedirs(folder)
    except OSError:
        if not os.path.isdir(folder):
            raise


def get_joblistfiles(unique_name, jobs, njobs):
    joblistfiles = []
    for i, task in enumerate(_chunks(jobs, njobs)):
        joblist = [j for j in task]
        jobfilename = unique_name + '_{:03d}'.format(i)
        with open(os.path.join(TASKFILEFOLDER, jobfilename), 'w') as f:
            f.write('\n'.join(joblist))
        joblistfiles.append(jobfilename)
    return joblistfiles


# -------- private functions


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


# -------- folder definitions
# these must be down here in order to use ensure_exist and _touch
# putting them in an extra file introduces circular dependencies -> cleaner solution?

LOCATION         = os.path.split(os.path.realpath(__file__))[0]
PENDINGJOBFOLDER = os.path.join(LOCATION, 'jobs/pending/')
ensure_exist(PENDINGJOBFOLDER)
RUNNINGJOBFOLDER = os.path.join(LOCATION, 'jobs/running/')
ensure_exist(RUNNINGJOBFOLDER)
DONEJOBFOLDER    = os.path.join(LOCATION, 'jobs/done/')
ensure_exist(DONEJOBFOLDER)
TASKFILEFOLDER   = os.path.join(LOCATION, 'jobs/tasks/')
ensure_exist(TASKFILEFOLDER)
JOBLISTFILE      = os.path.join(LOCATION, 'jobs/jobs')
_touch(JOBLISTFILE)
