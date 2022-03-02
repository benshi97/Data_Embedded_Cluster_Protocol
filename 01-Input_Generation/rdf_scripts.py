from ase import io
from ase.units import Bohr
from ase.visualize import view
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

def get_test_cluster(filename='',output_filename='cluster_test.xyz',M_element='Mg',O_element='O',fmt='pun',pbc='False',supercell=[10,10,1]):
    if fmt == 'pun':
        max = 1000
        f = open(output_filename,'w')
        f.write('{0}\n test\n'.format(max))
        with open(filename,'r') as infile:
            total_counter = 0
            i = 0
            while total_counter < max:

                a = infile.readline().split()
                if a[0] == M_element:
                    f.write('{0} {1:20.8f} {2:20.8f} {3:20.8f}\n'.format('{0}'.format(M_element),float(a[1])*Bohr,float(a[2])*Bohr, float(a[3])*Bohr))
                    total_counter += 1
                elif a[0] == O_element:
                    f.write('{0} {1:20.8f} {2:20.8f} {3:20.8f}\n'.format('O ',float(a[1])*Bohr,float(a[2])*Bohr, float(a[3])*Bohr))
                    total_counter += 1
                i += 1
        f.close()
    else:
        if pbc == True:
            a = io.read(filename,format=fmt)
            b = a*supercell
            io.write(output_filename,b)
        else:
            a = io.read(filename,format=fmt)
            io.write(output_filename,a)  

def get_atoms_list(M_list,a,MO_dist,filename):
    O_list = []

    for i in range(len(M_list)):
        for j in range(len(a)):
            if a[j].symbol == 'O' and np.linalg.norm(a[j].position - a[M_list[i]].position) < (MO_dist + 0.2):
                O_list += [j]

    total_list = list(set(M_list + O_list))
    io.write(filename,a[total_list],format='xyz') 
    return total_list

def get_rdf_cluster(filename='cluster_test.xyz',output_filename_append='',centre_index=0,MO_dist=2.10322906,M_element='Mg',num_rdf_clusters=10):
    a = io.read(filename)

    M_dist_list = []
    M_indices_list = []


    for i in range(len(a)):
        if a[i].symbol == M_element:
            atomic_dist = np.linalg.norm(a[i].position - a[centre_index].position)
            M_dist_list += ['{0:.3f}'.format(np.floor(atomic_dist * 1000)/1000)]
            M_indices_list += [i]

    
    unique_M_dist_list = [float(i) for i in list(set(M_dist_list))]
    unique_M_dist_list.sort()

    total_M_list = np.zeros((len(unique_M_dist_list)),dtype=int)

    num_M_list = np.zeros((len(unique_M_dist_list)),dtype=int)
    indices_M_list = []

    for i in range(len(unique_M_dist_list)):
        dummy_indices_list = []
        for j in range(len(M_dist_list)):
            if (abs(float(M_dist_list[j]) - unique_M_dist_list[i]) < 0.0015):
                num_M_list[i] += 1
                dummy_indices_list += [M_indices_list[j]]
        indices_M_list += [dummy_indices_list]
        total_M_list[i] = total_M_list[i-1] + num_M_list[i]

    cumulative_M_list = []
    cumulative_M_indices = []
    for i in range(num_rdf_clusters):
        cumulative_M_list = cumulative_M_list + indices_M_list[i]
        cumulative_M_indices += [get_atoms_list(cumulative_M_list,a,MO_dist,\
            'Structures/cluster_{0}_rdf_{1}.xyz'.format(output_filename_append,i+1))]

    rdf_x = [0]
    rdf_y = [0]

    for i in range(len(unique_M_dist_list)):
        rdf_x += [unique_M_dist_list[i]-0.05,unique_M_dist_list[i],unique_M_dist_list[i]+0.05]
        rdf_y += [0,num_M_list[i],0]
    fig, axs = plt.subplots(figsize=(3.37,2),dpi=1200, constrained_layout=True)
    
    peak_dist = [-0.05, 0.0, 0.05]

    for i in range(num_rdf_clusters):
        dummy2 = axs.plot([x + total_M_list[i] for x in peak_dist],[0,num_M_list[i],0],linewidth=1)
        axs.text(total_M_list[i],num_M_list[i]+0.8,'{0}'.format(i+1),horizontalalignment='center',verticalalignment='center',color=dummy2[0].get_color())

        

    # axs.set_xlabel(r'Distance from central atom, $r$ (\AA{})')
    axs.set_xlabel('Quantum cluster size (\# of {0} ions)'.format(M_element))

    axs.set_ylabel('RDF (\# of {0} ions)'.format(M_element))
    axs.set_title('{0} system'.format(output_filename_append))

    axs.set_xlim([0,total_M_list[num_rdf_clusters]])
    axs.set_ylim([0,np.max(num_M_list[:num_rdf_clusters]) + 2])
    print('YOU HAVE BEEN SKZCAMMED')
    plt.savefig('cluster_{0}_rdf_plot.png'.format(output_filename_append),format='png')
    plt.show()
    np.save('cluster_{0}_rdf_indices.npy'.format(output_filename_append),cumulative_M_indices)


def visualize_cluster(filename='Structures/cluster__rdf_1.xyz'):
    dummy1 = io.read('Structures/cluster_rdf_1.xyz')
    view(dummy1, viewer='x3d')