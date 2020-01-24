from __future__ import division

import json
import os

import numpy as np
import pandas

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt # noqa

from utils import _flatten_dictionary, _get_from_dict

def borders(points):
    out = np.zeros(len(points) + 1)
    out[1:-1] = (points[1:] + points[:-1]) / 2.
    out[0] = 2 * points[0] - out[1]
    out[-1] = 2 * points[-1] - out[-2]
    return out


def get_activity_from_pdata(pdata):
    weights     = np.array(sorted(set(pdata['parameters_network_weightparameters_weight'])))
    biasfactors = np.array(sorted(set(pdata['parameters_network_biasparameters_biasfactor'])))

    plot_weights     = borders(weights)
    plot_biasfactors = -borders(biasfactors)

    activities = -1 * np.ones((len(weights), len(biasfactors)))
    for pd in pdata.iterrows():
        i, = np.where(weights == pd[1]['parameters_network_weightparameters_weight'])
        j, = np.where(biasfactors == pd[1]['parameters_network_biasparameters_biasfactor'])
        activities[i, j] = pd[1]['actmean']

    activities = np.ma.masked_where(activities == -1, activities)

    return plot_weights, plot_biasfactors, activities


def plot_ising(pdatas, title, nneurons=6400):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for pdata in pdatas:
        plot_weights, plot_biasfactors, activities = get_activity_from_pdata(
                                                                        pdata)
        cax = ax.pcolor(plot_weights, plot_biasfactors, activities.T,
            vmin=0.3*nneurons, vmax=0.7*nneurons, edgecolors='k')
    fig.colorbar(cax)
    ax.set_title(title)
    ax.set_xlabel('BM weight')
    ax.set_ylabel('biasfactor')

    plt.savefig('z_meanact_{}.pdf'.format(title))


def get_pdatas(files, interesting_keys, analysis_keys):
    pdatas = []
    for fname in files:
        origdata = json.load(open(fname, 'r'))
        data = []
        for dd in origdata:
            if dd['results'] is None:
                continue
            outdict = {}
            analysisdict = dd['results']
            dd = _flatten_dictionary(dd)
            for k in interesting_keys:
                outdict[k] = dd[k]
            for k in analysis_keys:
                outdict[k] = analysisdict[k]
            data.append(outdict)
        pdatas.append(pandas.DataFrame(data))

    return pdatas


#rseedvariable = 'parameters_network_initialstateparameters_initialrseed'
#rseedvariable = 'parameters_backend_dicts_Config_randomSeed'
#rseedvariable = 'parameters_backend_dicts_Config_tauref'
rseedvariable = 'parameters_backend_dicts_Config_tausyn'

def plot_ising_runs(filepattern):
    interesting_keys = ['parameters_network_biasparameters_biasfactor',
                        'parameters_network_biasparameters_biasnoise',
                        'parameters_network_weightparameters_weight',
                        'parameters_network_weightparameters_weightnoise',
                        rseedvariable,
                       # 'parameters_backend_dicts_Config_synapseType',
                        ]
    analysis_keys = ['actmean']
    pdatas = get_pdatas(filepattern, interesting_keys, analysis_keys)

    #for bn in set(pdatas[0]['parameters_network_biasparameters_biasnoise']):
    #    for wn in set(pdatas[0]['parameters_network_weightparameters_weightnoise']):
    #        title = '{}_{}'.format(bn, wn)
    #        useddata = [pdata.loc[pdata['parameters_network_biasparameters_biasnoise']==bn] for pdata in pdatas]
    #        useddata = [ud.loc[ud['parameters_network_weightparameters_weightnoise']==wn] for ud in useddata]
    #        plot_ising(useddata, title)
    #return
    for rseed in set(pdatas[0][rseedvariable]):
        useddata = [pdata.loc[pdata[rseedvariable] == rseed] for pdata in pdatas]
   #     if len(set(useddata[0]['parameters_backend_dicts_Config_synapseType'])) != 1:
   #         raise ValueError("I do not plot different synapse types")
   #     title = set(useddata[0]['parameters_backend_dicts_Config_synapseType']).pop() + '_' + str(rseed) + '_' + '_'.join(os.path.basename(f) for f in filepattern)
        title = str(rseed)
   #     title = ''
        plot_ising(useddata, title)


def plot_ising_run(collected_data_file):
    orig_data = json.load(open(collected_data_file, 'r'))

    interesting_keys = ['parameters_network_biasparameters_biasfactor',
                        'parameters_network_weightparameters_weight',
                        rseedvariable,
                        'parameters_backend_dicts_Config_synapseType', ]
    analysis_keys = ['actmean', 'actstd']
    data = []

    for dd in orig_data:
        if dd['analysis'] is None:
            continue
        outdict = {}
        analysisdict = dd['analysis']
        for k in interesting_keys:
            outdict[k] = dd[k]
        for k in analysis_keys:
            outdict[k] = analysisdict[k]
        data.append(outdict)

    pdata = pandas.DataFrame(data)
    if len(set(pdata['Config_synapseType'])) != 1:
        raise ValueError('Can only deal with one synapse type')
    for rseed in set(pdata[rseedvariable]):
        plot_ising([pdata.loc[(pdata[rseedvariable] == rseed)]],
                pdata['Config_synapseType']+'_'+str(rseed))


if __name__ == '__main__':
    import sys
    plot_ising_runs(sys.argv[1:])
