import pandas as pd

import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 9})
import extrapolate

Hartree = 27.211386245988
Bohr = 0.5291772105638411


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
            search_word = 'Reference energy [au]:    '
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
            basis_list = ['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z']
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

    if code_format=='mrcc_can':
        if system=='TiO2':
            basis_list = ['SVP','TZVPP', 'QZVPP', 'CVTZ','VTZ','VQZ']
            #['SVP','TZVPP', 'QZVPP', 'CVTZ','CVQZ','CV5Z','VDZ','VTZ','VQZ','V5Z']

        energies_dict = dict.fromkeys(basis_list)

        for i in energies_dict:
            energies_dict[i] = {'perfect': {'hf': 0.0, 'ccsdt': 0.0, 'total': 0.0},
            'defect': {'hf': 0.0, 'ccsdt': 0.0, 'total': 0.0},
            'O': {'hf': 0.0, 'ccsdt': 0.0, 'total': 0.0},
            'vac_energy': {'hf': 0.0, 'ccsdt': 0.0, 'total': 0.0}}

        
        for index, i in enumerate(basis_list):
            for j in ['perfect','defect', 'O']:
                for k in ['hf','ccsdt']:
                    energies_dict[i][j][k] = find_energy('{0}/{1}/{2}/mrcc.out'.format(filepath,i,j),typ=k)
                energies_dict[i][j]['total'] = energies_dict[i][j]['hf'] + energies_dict[i][j]['ccsdt']

            energies_dict[i]['vac_energy']['hf'] = (energies_dict[i]['defect']['hf'] + energies_dict[i]['O']['hf'] - energies_dict[i]['perfect']['hf'])*Hartree
            energies_dict[i]['vac_energy']['ccsdt'] = (energies_dict[i]['defect']['ccsdt'] + energies_dict[i]['O']['ccsdt'] - energies_dict[i]['perfect']['ccsdt'])*Hartree
            energies_dict[i]['vac_energy']['total'] =  energies_dict[i]['vac_energy']['hf'] + energies_dict[i]['vac_energy']['ccsdt']
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

def get_energy_extrapolation(energies_dict,system='MgO',output=True,code_format='mrcc'):

    X = 'SVP'
    Y = 'TZVPP'

    a,b,cbs1 = extrapolate.get_cbs(energies_dict['SVP']['vac_energy']['hf'],energies_dict['SVP']['vac_energy']['lccsdt'],\
    energies_dict['TZVPP']['vac_energy']['hf'],energies_dict['TZVPP']['vac_energy']['lccsdt'],X=2,Y=3,family='def2',convert_Hartree=False,shift=0.0,output=False)

    X = 'TZVPP'
    Y = 'QZVPP'

    a,b,cbs2 = extrapolate.get_cbs(energies_dict['TZVPP']['vac_energy']['hf'],energies_dict['TZVPP']['vac_energy']['lccsdt'],\
    energies_dict['QZVPP']['vac_energy']['hf'],energies_dict['QZVPP']['vac_energy']['lccsdt'],X=3,Y=4,family='def2' ,convert_Hartree=False,shift=0.0,output=False)

    X = 'VDZ'
    Y = 'VTZ'

    a,b,cbs3 = extrapolate.get_cbs(energies_dict['VDZ']['vac_energy']['hf'],energies_dict['VDZ']['vac_energy']['lccsdt'],\
    energies_dict['VTZ']['vac_energy']['hf'],energies_dict['VTZ']['vac_energy']['lccsdt'],X=2,Y=3,family='mixcc',convert_Hartree=False,shift=0.0,output=False)

    X = 'VTZ'
    Y = 'VQZ'

    a,b,cbs4 = extrapolate.get_cbs(energies_dict[X]['vac_energy']['hf'],energies_dict[X]['vac_energy']['lccsdt'],\
    energies_dict[Y]['vac_energy']['hf'],energies_dict[Y]['vac_energy']['lccsdt'],X=3,Y=4,family='mixcc',convert_Hartree=False,shift=0.0,output=False)
    
    X = 'VQZ'
    Y = 'V5Z'

    a,b,cbs5 = extrapolate.get_cbs(energies_dict[X]['vac_energy']['hf'],energies_dict[X]['vac_energy']['lccsdt'],\
    energies_dict[Y]['vac_energy']['hf'],energies_dict[Y]['vac_energy']['lccsdt'],X=4,Y=5,family='mixcc',convert_Hartree=False,shift=0.0,output=False)

    if system=='MgO':
        X = 'CVDZ'
        Y = 'CVTZ'

        a,b,cbs6 = extrapolate.get_cbs(energies_dict[X]['vac_energy']['hf'],energies_dict[X]['vac_energy']['lccsdt'],\
        energies_dict[Y]['vac_energy']['hf'],energies_dict[Y]['vac_energy']['lccsdt'],X=2,Y=3,family='mixcc' ,convert_Hartree=False,shift=0.0,output=False)


    X = 'CVTZ'
    Y = 'CVQZ'

    a,b,cbs7 = extrapolate.get_cbs(energies_dict[X]['vac_energy']['hf'],energies_dict[X]['vac_energy']['lccsdt'],\
    energies_dict[Y]['vac_energy']['hf'],energies_dict[Y]['vac_energy']['lccsdt'],X=3,Y=4,family='mixcc',convert_Hartree=False ,shift=0.0,output=False)

    X = 'CVQZ'
    Y = 'CV5Z'

    a,b,cbs8 = extrapolate.get_cbs(energies_dict[X]['vac_energy']['hf'],energies_dict[X]['vac_energy']['lccsdt'],\
    energies_dict[Y]['vac_energy']['hf'],energies_dict[Y]['vac_energy']['lccsdt'],X=4,Y=5,family='mixcc',convert_Hartree=False ,shift=0.0,output=False)

    if output==True:
        print('{0:12s}: {1:12.7f}'.format('SVP/TZVPP',cbs1))
        print('{0:12s}: {1:12.7f}'.format('TZVPP/QZVPP',cbs2))
        print('{0:12s}: {1:12.7f}'.format('VDZ/VTZ',cbs3))
        print('{0:12s}: {1:12.7f}'.format('VTZ/VQZ',cbs4))
        print('{0:12s}: {1:12.7f}'.format('VQZ/V5Z',cbs5))

        if system=='MgO':
            print('{0:12s}: {1:12.7f}'.format('CVDZ/CVTZ',cbs6))
        
        print('{0:12s}: {1:12.7f}'.format('CVTZ/CVQZ',cbs7))
        print('{0:12s}: {1:12.7f}'.format('CVQZ/CV5Z',cbs8))

    if system=='MgO':
        return [cbs1,cbs2,cbs3,cbs4,cbs5,cbs6,cbs7,cbs8],['SVP/TZVPP','TZVPP/QZVPP','VDZ/VTZ','VTZ/VQZ','VQZ/V5Z','CVDZ/CVTZ','CVTZ/CVQZ','CVQZ/CV5Z']
    elif system=='TiO2' and code_format=='mrcc':
        return [cbs1,cbs2,cbs3,cbs4,cbs5,cbs7,cbs8],['SVP/TZVPP','TZVPP/QZVPP','VDZ/VTZ','VTZ/VQZ','VQZ/V5Z','CVTZ/CVQZ','CVQZ/CV5Z']


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
