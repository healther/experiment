"""Provide C&C capabilities for experiments

Basic workflow:
    ### TODO
"""
from __future__ import print_function, division

import collections
import copy
import glob
import os
import shutil
import warnings


def ensure_tracking(experiment_name, experimentfile):
    ensure_exist(os.path.join('simulations', '01_runs'))
    trackingFileName = os.path.join('simulations', '01_runs', experiment_name)
    if os.path.isfile(trackingFileName):
        response = raw_input("{} already exists. Do you want to override "
                             "it? [y/n/a]  ".format(trackingFileName))
        if response is "y":
            shutil.copy(experimentfile, trackingFileName)
        elif response is "n":
            pass
        else:
            print("Aborting")
            exit()
    else:
        shutil.copy(experimentfile, trackingFileName)


def ensure_exist(folder):
    try:
        os.makedirs(folder)
    except OSError:
        if not os.path.isdir(folder):
            raise


def ensure_is_empty(folder):
    for f in glob.glob(folder + '/*'):
        os.remove(f)


def expanddict(dict_to_expand, expansions, rules):
    """Return a list of copies of dict_to_expand with a kartesian product of
             all expansions.

    Input:
        dict_to_expand: dictionary with values to replace
        expansions: dictionary of {"identifier": [values]} tuples
        rules: dictionary of restrictions TODO: add description

    Output:
        expanded_dicts: list of dictionaries with all expansions due to the
                            kartesian product of the modifier values

    >>> d = { 1: 'blub', 2: {3: 'blub', 4: 'hello'}}
    >>> e = {'blub': ['a', 'b'], 'hello': [11, 12]}
    >>> expanddict(d, e, {})
    [{1: 'a', 2: {3: 'a', 4: 11}}, {1: 'b', 2: {3: 'b', 4: 11}}, {1: 'a', 2: {3: 'a', 4: 12}}, {1: 'b', 2: {3: 'b', 4: 12}}]
    """
    expanded_dicts = [dict_to_expand]
    for ident, values in expansions.items():
        keypositions = _find_key_from_identifier(dict_to_expand, ident)
        tmp = []
        for d in expanded_dicts:
            for v in values:
                for kp in keypositions:
                    _update_dict(d, v, *kp)
                tmp.append(copy.deepcopy(d))
        expanded_dicts = tmp

    return_dicts = [exdict for exdict in expanded_dicts
                           if not _violate_any(exdict, rules)]

    return return_dicts


def generate_folder_template(replacement_dictionary, expanding_dictonary,
            base='simulations', experimentname=''):
    entries = []
    for replacement_id in replacement_dictionary.keys():
        keys = _find_key_from_identifier(
                    _flatten_dictionary(expanding_dictonary), replacement_id)
        # keys is a list of lists, i.e. keys[0] contains the list of nested
        # keys at which we find the replacement_id, due to the flattening,
        # this key has only length 1.
        entry = '{' + keys[0][0] + '}'
        entries.append(entry)

    return os.path.join(base, experimentname, "_".join(entries))


def get_folders(ex_dicts, sim_folder_template):
    """Helper function providing the simulation folder from the template."""
    folders = [sim_folder_template.format(**d)
                    for d in map(_flatten_dictionary, ex_dicts)]
    return folders


def get_jobs(folders):
    jobfiles = []
    for folder in folders:
        jobfilename = os.path.join(folder, 'job')
        if os.path.exists(jobfilename):
            jobfiles.append(jobfilename)
        else:
            warnings.warn("Missing jobfile in {}".format(folder))
    return jobfiles


# ------ private functions ------

def _find_key_from_identifier(dict_to_expand, identifier):
    """Return a list of keys to all leaves of dict_to_expand whose values are
            identifier.

    >>> d = { 1: 'blub', 2: {3: 'blub', 4: 'hello'}}
    >>> _find_key_from_identifier(d, 'blub')
    [[1], [2, 3]]
    """
    keypositions = []
    for k, v in dict_to_expand.items():
        if v == identifier:
            keypositions.append([k])
        elif isinstance(v, dict):
            subkey_positions = _find_key_from_identifier(v, identifier)
            for sk in subkey_positions:
                keypositions.append([k] + sk)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if x == identifier:
                    keypositions.append([k] + [i])

    return keypositions


def _flatten_dictionary(d, parent_key='', sep='_'):
    """Return a flat dictionary with concatenated keys for a nested dictionary d.

    >>> d = { 'a': {'aa': 1, 'ab': {'aba': 11}}, 'b': 2, 'c': {'cc': 3}}
    >>> _flatten_dictionary(d)
    {'a_aa': 1, 'b': 2, 'c_cc': 3, 'a_ab_aba': 11}

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(_flatten_dictionary(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def _update_dict(dic, value, key, *keys):
    """Set dic[k0][k1]...[kn] = value for keys=[k0, k1, ..., kn].

    >>> d = { 1: 'blub', 2: {3: 'blub', 4: 'hello'}}
    >>> keys = _find_key_from_identifier(d, 'blub')
    >>> keys
    [[1], [2, 3]]
    >>> _update_dict(d, 'ch', *keys[0])
    >>> d
    {1: 'ch', 2: {3: 'blub', 4: 'hello'}}
    >>> _update_dict(d, 'ch', *keys[1])
    >>> d
    {1: 'ch', 2: {3: 'ch', 4: 'hello'}}
    """
    if keys:
        _update_dict(dic[key], value, *keys)
    else:
        dic[key] = value


def _violate_any(dic, rules):
    for rule in rules:
        factor1 = _get_from_dict(dic, rules[0])
        factor2 = _get_from_dict(dic, rules[1])
        operator = rules[2]
        if _violate(operator, factor1, factor2):
            return True


def _violate(operator, factor1, factor2):
    if operator == '==':
        return factor1 != factor2
    elif operator == '<':
        return factor1 >= factor2
    elif operator == '>':
        return factor1 <= factor2
    else:
        raise NotImplementedError('No rule for {} implemented'
                                  ''.format(operator))


def _get_from_dict(dataDict, key, *keys):
    """Recursive get from nested dicts

    >>> d = { 1: {2: 'blub', 3: 'argh'}, 4: {5: 'use'}}
    >>> _get_from_dict(d, 1, 3)
    'argh'
    >>> _get_from_dict(d, 4, 5)
    'use'
    """
    if keys:
        return _get_from_dict(dataDict[key], *keys)
    else:
        return dataDict[key]


if __name__ == '__main__':
    import doctest
    import sys
    res = doctest.testmod()
    print(res)
    sys.exit(res[0])
