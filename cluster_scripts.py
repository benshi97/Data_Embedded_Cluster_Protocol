from ase import io
import ase
import math
from ase.units import Hartree,Bohr
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

import numpy as np
from scipy.stats import norm
from scipy import stats
import matplotlib.mlab as mlab
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import AutoMinorLocator
import matplotlib as mpl
mpl.use("pgf")
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "font.size": 9,
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.preamble": [        # load additional packages 
         "\\usepackage{amsmath}",  
         "\\usepackage{amssymb}",  
         "\\usepackage[mathrm=sym]{unicode-math}", # unicode math setup
         r"\setmathfont{FiraMath-Regular.otf}",
         r"\setmainfont[BoldFont={FiraSans-SemiBold.otf}]{FiraSans-Regular.otf}",
         r"\setmathfont[version=bold]{FiraMath-Bold.otf}",
         r"\newcommand{\minus}{\scalebox{0.5}[1.0]{$-$}}" # serif font via preamble
         ]
})
import extrapolate


color_dict = {'red':'#e6194b',
'green': '#3cb44b',
'yellow': '#ffe119',
'blue': '#4363d8',
'orange': '#f58231',
'purple': '#911eb4',
'cyan':  '#42d4f4',
'magenta': '#f032e6',
'lime':  '#bfef45',
'pink': '#fabed4',
'teal': '#469990',
'lavendar': '#dcbeff',
'brown': '#9A6324',
'beige':'#fffac8',
'maroon':'#800000',
'mint': '#aaffc3',
'olive': '#808000',
'apricot':'#ffd8b1', 
'navy':'#000075',
'grey': '#a9a9a9',
'white': '#ffffff', 
'black':'#000000'}

plt.rcParams["axes.prop_cycle"] = plt.cycler(color=['#4363d8', '#e6194B', '#3cb44b', '#f58231', '#ffe119', '#911eb4', '#42d4f4', \
'#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', \
'#000075', '#a9a9a9', '#ffffff', '#000000'])


def find_energy(filename,typ='ccsdt',code_format='mrcc'):

    if code_format=='mrcc':
        if typ == 'lccsdt':
            search_word = 'CCSD(T) correlation energy + MP2 corrections [au]:'
        elif typ == 'ccsdt':
            search_word = 'CCSD(T) correlation energy [au]:'
        elif typ == 'hf':
            search_word = 'Reference energy [au]:          '
        elif typ == 'lmp2':
            search_word = 'LMP2 correlation energy [au]:         '
        elif typ == 'mp2':
            search_word = 'MP2 correlation energy [au]:   '
        elif typ == 'lccsd':
            search_word = 'CCSD correlation energy + 0.5 MP2 corrections [au]:'
        elif typ == 'ccsd':
            search_word = 'CCSD correlation energy [au]: '
        elif typ == 'dft':
            search_word = '***FINAL KOHN-SHAM ENERGY:'
        elif typ == 'B2PLYP':
            search_word = 'MP2 contribution [au]:'
        elif typ == 'DSDPBEP86':
            search_word = 'SCS-MP2 contribution [au]:'

        
        
        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            if typ == 'dft':
                return float(a[-1].split()[-2])
            else:
                return float(a[-1].split()[-1])
    elif code_format=='orca':
        if typ == 'lccsdt':
            search_word = 'Final correlation energy'
        # elif typ == 'ccsdt':
        #     search_word = 'CCSD(T) correlation energy [au]:'
        elif typ == 'hf':
            search_word = 'E(0)'
        elif typ == 'lmp2':
            search_word = 'E(SL-MP2) including corrections'
        # elif typ == 'mp2':
        #     search_word = 'MP2 correlation energy [au]:   '
        elif typ == 'lccsd':
            search_word = 'E(CORR)(corrected)'
        # elif typ == 'ccsd':
        #     search_word = 'CCSD correlation energy [au]: '        
        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-1])

    elif code_format=='orca_mp2':
        if typ == 'lccsdt':
            search_word = 'Final correlation energy'
        # elif typ == 'ccsdt':
        #     search_word = 'CCSD(T) correlation energy [au]:'
        elif typ == 'hf':
            search_word = 'Total energy after final integration'
        elif typ == 'lmp2':
            search_word = 'DLPNO-MP2 CORRELATION ENERGY'
        # elif typ == 'mp2':
        #     search_word = 'MP2 correlation energy [au]:   '
        elif typ == 'lccsd':
            search_word = 'E(CORR)(corrected)'
        # elif typ == 'ccsd':
        #     search_word = 'CCSD correlation energy [au]: '

        
        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-2])

def get_energy(filepath,system='MgO',basis_list =['SVP','TZVPP', 'QZVPP', 'CVDZ','CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z'],code_format='mrcc'):
    if code_format=='mrcc':
        if system=='TiO2':
            basis_list = ['SVP','TZVPP', 'QZVPP', 'CVTZ','VTZ','VQZ']
            #['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z']

        energies_dict = dict.fromkeys(basis_list)

        for i in energies_dict:
            energies_dict[i] = {'perfect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0,'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'defect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'O': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'vac_energy': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0}}

        
        for index, i in enumerate(basis_list):
            for j in ['perfect','defect', 'O']:
                for k in ['hf','lmp2','lccsd','lccsdt']:
                    if j == 'O' and k == 'lccsdt':
                        energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/mrcc.out'.format(filepath,i,j),typ='ccsdt')
                    elif j == 'O' and k == 'lmp2':
                        energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/mrcc.out'.format(filepath,i,j),typ='mp2')
                    elif j == 'O' and k == 'lccsd':
                        energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/mrcc.out'.format(filepath,i,j),typ='ccsd')
                    else:
                        energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/mrcc.out'.format(filepath,i,j),typ=k)

                energies_dict[i][j]['total_lmp2'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lmp2']
                energies_dict[i][j]['total_lccsd'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lccsd']
                energies_dict[i][j]['total_lccsdt'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lccsdt']

            energies_dict[i]['vac_energy']['hf'] = (energies_dict[i]['defect']['hf'] + energies_dict[i]['O']['hf'] - energies_dict[i]['perfect']['hf'])*Hartree
            for l in ['lmp2','lccsd','lccsdt']:
                energies_dict[i]['vac_energy'][l] = (energies_dict[i]['defect'][l] \
                    + energies_dict[i]['O'][l] - energies_dict[i]['perfect'][l])*Hartree
                energies_dict[i]['vac_energy']['total_{0}'.format(l)] =  energies_dict[i]['vac_energy']['hf'] + energies_dict[i]['vac_energy'][l]

        return energies_dict

    elif code_format=='orca':
        if system=='TiO2':
            basis_list = ['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','VTZ','VQZ','SVPD','TZVPPD','QZVPPD']
            #['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z']

        energies_dict = dict.fromkeys(basis_list)

        for i in energies_dict:
            energies_dict[i] = {'perfect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0,'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'defect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'O': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'vac_energy': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0}}
        
        for index, i in enumerate(basis_list):
            for j in ['perfect','defect', 'O']:
                for k in ['hf','lmp2','lccsd','lccsdt']:
                    energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/orca.out'.format(filepath,i,j),typ=k,code_format='orca')
                energies_dict[i][j]['total_lmp2'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lmp2']

                energies_dict[i][j]['total_lccsd'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lccsd']
                energies_dict[i][j]['total_lccsdt'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lccsdt']

            energies_dict[i]['vac_energy']['hf'] = (energies_dict[i]['defect']['hf'] + energies_dict[i]['O']['hf'] - energies_dict[i]['perfect']['hf'])*Hartree
            for l in ['lmp2','lccsd','lccsdt']:
                energies_dict[i]['vac_energy'][l] = (energies_dict[i]['defect'][l] \
                    + energies_dict[i]['O'][l] - energies_dict[i]['perfect'][l])*Hartree
                energies_dict[i]['vac_energy']['total_{0}'.format(l)] =  energies_dict[i]['vac_energy']['hf'] + energies_dict[i]['vac_energy'][l]
        return energies_dict

    elif code_format=='orca_mp2':
        if system=='TiO2':
            basis_list = ['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','VTZ','VQZ','SVPD','TZVPPD','QZVPPD']
            #['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z']

        energies_dict = dict.fromkeys(basis_list)

        for i in energies_dict:
            energies_dict[i] = {'perfect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0,'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'defect': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'O': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0},
            'vac_energy': {'hf': 0.0, 'lmp2': 0.0,'lccsd': 0.0, 'lccsdt': 0.0, 'total_lmp2': 0.0, 'total_lccsd': 0.0, 'total_lccsdt': 0.0}}
        
        for index, i in enumerate(basis_list):
            for j in ['perfect','defect', 'O']:
                for k in ['hf','lmp2']:
                    energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/orca.out'.format(filepath,i,j),typ=k,code_format='orca_mp2')
                energies_dict[i][j]['total_lmp2'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['lmp2']

            energies_dict[i]['vac_energy']['hf'] = (energies_dict[i]['defect']['hf'] + energies_dict[i]['O']['hf'] - energies_dict[i]['perfect']['hf'])*Hartree
            for l in ['lmp2']:
                energies_dict[i]['vac_energy'][l] = (energies_dict[i]['defect'][l] \
                    + energies_dict[i]['O'][l] - energies_dict[i]['perfect'][l])*Hartree
                energies_dict[i]['vac_energy']['total_{0}'.format(l)] =  energies_dict[i]['vac_energy']['hf'] + energies_dict[i]['vac_energy'][l]

        return energies_dict


# Scripts for calculating the cWFT corrections at the different levels of theory and systems

def get_corr_mrcc(filename,method):
    data_smaller_def2 = get_energy('{0}'.format(filename),basis_list=['TZVPP','QZVPP'])
    data_smaller_def2_cbs = extrapolate.get_cbs(data_smaller_def2['TZVPP']['vac_energy']['hf'],data_smaller_def2['TZVPP']['vac_energy'][method],\
        data_smaller_def2['QZVPP']['vac_energy']['hf'],data_smaller_def2['QZVPP']['vac_energy'][method],X=3,Y=4,family='def2',convert_Hartree=False ,shift=-5.21/2,output=False)

    data_smaller_cc = get_energy('{0}'.format(filename),basis_list=['CVTZ','CVQZ'])
    data_smaller_cc_cbs = extrapolate.get_cbs(data_smaller_cc['CVTZ']['vac_energy']['hf'],data_smaller_cc['CVTZ']['vac_energy'][method],\
            data_smaller_cc['CVQZ']['vac_energy']['hf'],data_smaller_cc['CVQZ']['vac_energy'][method],X=3,Y=4,family='mixcc',convert_Hartree=False ,shift=-5.21/2,output=False)
    # print(data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2])
    return data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2]

def get_corr_mrcc_b2plyp(folder):
    ene_vac_hf = []
    ene_vac_mp2 = []
    i='B2PLYP'
    for j in ['TZ','QZ']:
        ene_perfect = find_energy('{0}/CV{1}/perfect/mrcc.out'.format(folder,j),typ='hf')
        ene_defect = find_energy('{0}/CV{1}/defect/mrcc.out'.format(folder,j),typ='hf')
        ene_O = find_energy('{0}/CV{1}/O/mrcc.out'.format(folder,j),typ='hf')
        ene_vac_hf += [(ene_defect + ene_O - ene_perfect)*Hartree]
        ene_perfect = find_energy('{0}/CV{1}/perfect/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_defect = find_energy('{0}/CV{1}/defect/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_O = find_energy('{0}/CV{1}/O/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_vac_mp2 += [(ene_defect + ene_O - ene_perfect)*Hartree]
    # print(ene_vac_hf,ene_vac_mp2)
    data_smaller_cc_cbs = extrapolate.get_cbs(ene_vac_hf[0],ene_vac_mp2[0],ene_vac_hf[1],ene_vac_mp2[1],X=3,Y=4,family='mixcc',output=False)
    ene_vac_hf = []
    ene_vac_mp2 = []
    i='B2PLYP'
    for j in ['TZ','QZ']:
        ene_perfect = find_energy('{0}/{1}VPP/perfect/mrcc.out'.format(folder,j),typ='hf')
        ene_defect = find_energy('{0}/{1}VPP/defect/mrcc.out'.format(folder,j),typ='hf')
        ene_O = find_energy('{0}/{1}VPP/O/mrcc.out'.format(folder,j),typ='hf')
        ene_vac_hf += [(ene_defect + ene_O - ene_perfect)*Hartree]
        ene_perfect = find_energy('{0}/{1}VPP/perfect/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_defect = find_energy('{0}/{1}VPP/defect/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_O = find_energy('{0}/{1}VPP/O/mrcc.out'.format(folder,j),typ='{0}'.format(i))
        ene_vac_mp2 += [(ene_defect + ene_O - ene_perfect)*Hartree]
    # print(ene_vac_hf,ene_vac_mp2)

    data_smaller_def2_cbs = extrapolate.get_cbs(ene_vac_hf[0],ene_vac_mp2[0],ene_vac_hf[1],ene_vac_mp2[1],X=3,Y=4,family='def2',output=False)
    return (data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2])    

def get_corr_TiO2_surf(filename,method):

    if method=='lmp2':
        data_smaller = get_energy(filename,system='MgO',basis_list=['TZVPP','QZVPP','CVTZ','CVQZ'],code_format='orca_mp2')
    else:
        data_smaller = get_energy(filename,system='MgO',basis_list=['TZVPP','QZVPP','CVTZ','CVQZ'],code_format='orca')
    data_smaller_def2_cbs = extrapolate.get_cbs(data_smaller['TZVPP']['vac_energy']['hf'],data_smaller['TZVPP']['vac_energy'][method],\
        data_smaller['QZVPP']['vac_energy']['hf'],data_smaller['QZVPP']['vac_energy'][method],X=3,Y=4,family='def2',convert_Hartree=False ,shift=-5.21/2,output=False)

    data_smaller_cc_cbs = extrapolate.get_cbs(data_smaller['CVTZ']['vac_energy']['hf'],data_smaller['CVTZ']['vac_energy'][method],\
            data_smaller['CVQZ']['vac_energy']['hf'],data_smaller['CVQZ']['vac_energy'][method],X=3,Y=4,family='mixcc',convert_Hartree=False ,shift=-5.21/2,output=False)
    # print(data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2])
    return (data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2])

def get_corr_TiO2_Surf_b2plyp(folder):
    ene_vac_hf = []
    ene_vac_mp2 = []
    i='lmp2'
    for j in ['TZ','QZ']:
        ene_perfect = find_energy('{0}/CV{1}/perfect/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_defect = find_energy('{0}/CV{1}/defect/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_O = find_energy('{0}/CV{1}/O/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_vac_hf += [(ene_defect + ene_O - ene_perfect)*Hartree]
        ene_perfect = find_energy('{0}/CV{1}/perfect/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        ene_defect = find_energy('{0}/CV{1}/defect/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        ene_O = find_energy('{0}/CV{1}/O/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        # print(ene_perfect,ene_defect,ene_O)
        ene_vac_mp2 += [(ene_defect + ene_O - ene_perfect)*Hartree]
    data_smaller_cc_cbs = extrapolate.get_cbs(ene_vac_hf[0],ene_vac_mp2[0],ene_vac_hf[1],ene_vac_mp2[1],X=3,Y=4,family='mixcc',output=False)
    ene_vac_hf = []
    ene_vac_mp2 = []
    i='lmp2'
    for j in ['TZ','QZ']:
        ene_perfect = find_energy('{0}/{1}VPP/perfect/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_defect = find_energy('{0}/{1}VPP/defect/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_O = find_energy('{0}/{1}VPP/O/orca.out'.format(folder,j),typ='hf',code_format='orca_mp2')
        ene_vac_hf += [(ene_defect + ene_O - ene_perfect)*Hartree]
        ene_perfect = find_energy('{0}/{1}VPP/perfect/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        ene_defect = find_energy('{0}/{1}VPP/defect/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        ene_O = find_energy('{0}/{1}VPP/O/orca.out'.format(folder,j),typ='{0}'.format(i),code_format='orca_mp2')
        # print(ene_perfect,ene_defect,ene_O)
        ene_vac_mp2 += [(ene_defect + ene_O - ene_perfect)*Hartree]
    data_smaller_def2_cbs = extrapolate.get_cbs(ene_vac_hf[0],ene_vac_mp2[0],ene_vac_hf[1],ene_vac_mp2[1],X=3,Y=4,family='def2',output=False)
    return (data_smaller_cc_cbs[2], data_smaller_def2_cbs[2],data_smaller_cc_cbs[2] - data_smaller_def2_cbs[2])


# Scripts for parsing energy from MRCC and ORCA DFT calculations
def get_dft_vac_energy(folder):
    perfect_ene = get_mrcc_ene('{0}/perfect/mrcc.out'.format(folder))
    defect_ene = get_mrcc_ene('{0}/defect/mrcc.out'.format(folder))
    O_ene = get_mrcc_ene('{0}/O/mrcc.out'.format(folder))
    vac_ene = (defect_ene + O_ene - perfect_ene)*Hartree
    return vac_ene

def get_dft_vac_energy_orca(folder):
    perfect_ene = get_orca_ene('{0}/perfect/orca.out'.format(folder))
    defect_ene = get_orca_ene('{0}/defect/orca.out'.format(folder))
    O_ene = get_mrcc_ene('{0}/O/mrcc.out'.format(folder))
    vac_ene = (defect_ene + O_ene - perfect_ene)*Hartree
    return vac_ene

def get_dft_vac_energy_orca_mgo_bulk(folder):
    perfect_ene = get_orca_ene('{0}/perfect/orca.out'.format(folder))
    defect_ene = get_orca_ene('{0}/defect/orca.out'.format(folder))
    O_ene = get_orca_ene('{0}/O/orca.out'.format(folder))
    vac_ene = (defect_ene + O_ene - perfect_ene)*Hartree
    return vac_ene


def get_mrcc_ene(filename):
    with open(filename) as f:
        a = []
        for line in f.readlines():
                if 'FINAL KOHN' in line:
                    a += [float(line.split()[3])]
    return a[-1]

def get_orca_ene(filename):
    with open(filename) as f:
        a = []
        for line in f.readlines():
                if 'FINAL' in line:
                    a += [float(line.split()[-1])]
    return a [-1]  
