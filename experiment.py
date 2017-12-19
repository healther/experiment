"""Provide C&C capabilities for experiments

Basic workflow:
    ### TODO
"""
from __future__ import print_function, division

import datetime
import os

import json
import yaml

import jobcontrol
import utils


stub = """
#!/usr/bin/env bash

set -x
cd "{folder}" &&
set +x
source {envscript} &&
set -x
{executable} "{folder}/sim.json" &&
/usr/bin/touch "{folder}/success"
"""


def summarize(experiment_name, folders, quiet=False):
    output = []
    print("{}: Collecting {} results".format(datetime.datetime.now(), len(folders)))
    for i, folder in enumerate(folders):
        try:
            output.append(json.load(open(os.path.join(folder, 'analysis'), 'r')))
        except IOError: # no useable analysis file
            continue
        if not quiet:
            print("Collecting {: 3.1f}% complete".format(100*i/len(folders)), end='\r')
    print("{}: Collected {} results".format(datetime.datetime.now(), len(output)))

    utils.ensure_exist('collect')
    with open(os.path.join('collect', experiment_name), 'w') as f:
        json.dump(output, f)


def main(experimentfile, generate_sims, execute_sims, check_sims,
         summarize_sims, quiet=False):
    experiment_dict = yaml.load(open(experimentfile, 'r'))

    execution_params = experiment_dict.pop('executionParams')

    replacements = experiment_dict.pop('replacements', {})
    rules = experiment_dict.pop('rules', {})
    experiment_name = experiment_dict.pop('experimentName', '')
    executable = experiment_dict.pop('executable')
    envscript = experiment_dict.pop('envscript')
    basefolder = experiment_dict.pop('basefolder',
                                os.path.dirname(os.path.realpath(__file__)))

    utils.ensure_tracking(experiment_name, experimentfile, quiet=quiet)

    stub_dict = experiment_dict.pop('stub')

    sim_folder_template = utils.generate_folder_template(
                                    replacements, stub_dict,
                                    os.path.join(basefolder, 'simulations'),
                                    experiment_name)
    stub_dict['folderTemplate'] = sim_folder_template

    sim_dicts = [ex_stub_dict for ex_stub_dict in utils.expanddict(
                                            stub_dict, replacements, rules)]
    sim_folders = utils.get_folders(sim_dicts, sim_folder_template)

    if generate_sims:
        for i, (folder, sdict) in enumerate(zip(sim_folders, sim_dicts)):
            content = stub.format(folder=folder, envscript=envscript,
                                  executable=executable)
            utils.ensure_is_empty(folder)
            utils.ensure_exist(folder)
            with open(os.path.join(folder, 'job'), 'w') as f:
                f.write(content)
            sdict['folder'] = folder
            with open(os.path.join(folder, 'sim.json'), 'w') as f:
                json.dump(sdict, f)

    if execute_sims:
        jobs = utils.get_jobs(sim_folders)
        jobcontrol.execute(jobs, **execution_params)

    if check_sims:
        raise NotImplementedError()

    if summarize_sims:
        summarize(experiment_name, sim_folders, quiet=quiet)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='CnC for experiment.')
    parser.add_argument('experimentfile', type=str)

    parser.add_argument('--generate-sims', '-g', dest='generate_sims',
                    action='store_const', const=True, default=False,)
    parser.add_argument('--execute-sims', '-e', dest='execute_sims',
                    action='store_const', const=True, default=False,)
    parser.add_argument('--check-sims', '-c', dest='check_sims',
                    action='store_const', const=True, default=False,)
    parser.add_argument('--summarize-sims', '-s', dest='summarize_sims',
                    action='store_const', const=True, default=False,)
    parser.add_argument('--quiet', '-q', dest='quiet',
                    action='store_const', const=True, default=False,)

    args = parser.parse_args()
    main(**vars(args))
