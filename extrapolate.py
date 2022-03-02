#!/usr/bin/env python
# coding: utf-8

# In[44]:


# Script for performing basis set extrapolation of HF and correlation energies for both the cc
import numpy as np
from ase.units import Hartree


# In[45]:


def get_cbs(hf_X, corr_X, hf_Y, corr_Y, X=2, Y=3, family='cc', convert_Hartree=False,shift=0.0,output=True):
    alpha_dict = {
        "def2_2_3": 10.39,
        "def2_3_4": 7.88,
        "cc_2_3": 4.42,
        "cc_3_4": 5.46,
        "cc_4_5": 5.46,
        "acc_2_3": 4.30,
        "acc_3_4": 5.79,
        "acc_4_5": 5.79,
        "mixcc_2_3": 4.36,
        "mixcc_3_4": 5.625,
        "mixcc_4_5": 5.625
    }

    beta_dict = {
        "def2_2_3": 2.40,
        "def2_3_4": 2.97,
        "cc_2_3": 2.46,
        "cc_3_4": 3.05,
        "cc_4_5": 3.05,
        "acc_2_3": 2.51,
        "acc_3_4": 3.05,
        "acc_4_5": 3.05,
        "mixcc_2_3": 2.485,
        "mixcc_3_4": 3.05,
        "mixcc_4_5": 3.05
    }

    if Y != X+1:
        print('Y does not equal X+1')

    if family != 'cc' and family != 'def2' and family != 'acc' and family != 'mixcc':
        print('Wrong basis set family stated')

    alpha = alpha_dict['{0}_{1}_{2}'.format(family, X, Y)]
    beta = beta_dict['{0}_{1}_{2}'.format(family, X, Y)]

    hf_cbs = hf_X - np.exp(-alpha*np.sqrt(X))*(hf_Y - hf_X) / \
        (np.exp(-alpha*np.sqrt(Y))-np.exp(-alpha*np.sqrt(X)))
    corr_cbs = (X**(beta)*corr_X - Y**(beta)*corr_Y)/(X**(beta)-Y**(beta))
    if convert_Hartree == True:
        if output==True:
            print('CBS({0}/{1}) HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}'.format(X,Y, hf_cbs*Hartree + shift, corr_cbs*Hartree , (hf_cbs+corr_cbs)*Hartree + shift))
        return hf_cbs*Hartree + shift, corr_cbs*Hartree, (hf_cbs+corr_cbs)*Hartree
    else:
        if output==True:
            print('CBS({0}/{1})  HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}'.format(X,Y, hf_cbs + shift, corr_cbs, (hf_cbs+corr_cbs) + shift))
        return hf_cbs + shift, corr_cbs, (hf_cbs+corr_cbs) + shift
# %%
