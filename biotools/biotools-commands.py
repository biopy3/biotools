"""
This script is handle biotext!
"""

import os, sys, shutil, subprocess, multiprocessing
import re, platform


def set_softwarePATH():
    try:
        this_script_name = sys.argv[0]
        this_script_dir_name = os.path.dirname(this_script_name)
        abspath = os.path.abspath(this_script_dir_name)
        if os.name == 'posix' and sys.version_info[0] == 3:
            os.environ['PATH'] += ':' + abspath + '/softwares'
            os.environ['PATH'] += ':' + abspath + '/locarna-1.9.2/bin'
    except:
        print("Sorry, this program can't add softwares path to \"PATH\" env.")

def get_files_fullPath(directory_path, patterns):
    file_paths = []
    
    if os.path.isdir(directory_path):
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for pattern in patterns:
                for filename in filenames:
                    status = re.search(pattern, filename, flags=0)
                    if status:
                        file_paths.append(os.path.join(dirpath, filename))
        return file_paths
    else:
        print("First number must be a full path of dirctory!")
        return file_paths

def siut_same_name_dir(paths):
    try:
        for i in paths:
            os.mkdir(os.path.splitext(i)[0])
            shutil.move(i, os.path.splitext(i)[0])
    except:
        print("Have perssion mkdir or you given a wrong list of path!")

def get_dir_fullpath():
    return input("Please drog a dirctory to here:").strip().strip('\'')

def RNAalifold2fas_struct_rna(file_paths):
    for file_path in file_paths:
        seq_name_list = []
        seq_list = []
        fasta_file = open(os.splitext(file_path)[0] + '.fa', 'w')
        struc_file = open(os.splitext(file_path)[0] + '.structure.txt', 'w')
        rna_file = open(os.splitext(file_path)[0] + '.rna', 'w')
                     
        f = open(file_path, 'r')
        for i in range(9): # The likely all RNAalifold file in first nine lines 
            f.readline()   # For dump the first nine file in every file
        done = 0
        while not done:
            line = f.readline()
            if line == '':
                done = 1 # stop read, since touch the end of file
                continue
            line = line.strip()
            line_list = line.split()
            if line :
                if line_list[0] == 'alifold':
                    struc_file.write(line_list[1])
                elif line_list[0][0] == '.' or line_list[0][0] == '(':
                     struc_file.write(line_list[0])
                elif line_list[0] not in seq_name_list:
                     seq_list.append(line_list[1])
                     seq_name_list.append(line_list[0])
                elif line_list[0] in seq_name_list:
                     index = seq_list.index(line_list[0])
                     seq_list[index] += line_list[1]
                else:
                     pass

        struc_file.close()
        rna_file.write(str(len(seq_name_list)+' '+str(len(seq_list[0]))+' STRUCT\n\n'))
        rna_file.write(seq_name_list[i] + '\t' + seq_list[i] + '\n\n')         
        for i in range(len(seq_name_list)):         
            fasta_file.writelines(seq_name_list[i] + '\t' + seq_list[i])
            rna_file.writelines(seq_name_list[i] + '\t' + seq_list[i])
        fasta_file.close()
        rna_file.close()
    return 0

def model_select(file_path):
    try:
        subprocess.call(['perl','model_select.pl','--a', file_path, '--s', os.path.splitext(file_path)+'.struct',
                         '--t', os.path.splitext(file_path)+'.tree.txt', '--phase_o', '../softwares/rna-phase3.0/mcmcphase_Linux64bit',
                         '--phase_m', '../softwares/rna-phase3.0/mcmcphase_Linux64bit']) ####!!!!!!!!
    except:
        print("model_select.pl script fails, please check!")

def mmodel_select(file_paths):
    pool = multiprocessing.Pool(processes=len(file_paths))
    pool.map(model_select, file_paths)


def clustalw(file_path):
    #try:
    print(os.getcwd())
    print(os.environ['PATH'])
    subprocess.call(['clustalw2.1-Linux64bit', "-INFILE="+file_path, "-ALIGN", "-QUIET",
                     "-OUTPUT=FASTA", "-OUTFILE="+os.path.splitext(file_path)[0]+'_aln.fasta'])
    os.remove(os.path.splitext(file_path)[0]+'.dnd')
    #except:
    #print("This file is wrong:"+file_path.split('/')[-1])               

def mclustalw(file_paths):
    pool = multiprocessing.Pool(processes=len(file_paths))
    pool.map(clustalw, file_paths)
    print("Clustalw all finished!!!!!")

def phyml(file_path):
    try:
        subprocess.call(['PhyML-3.1_Linux64bit', '-i', file_path, '-b','500', '-m', 'GTR','-t','e',"--quiet"])
    except:
        print("This file is wrong:"+file.split('/')[-1])

def mphyml(file_paths):
    pool = multiprocessing.Pool(processes=len(file_paths))
    pool.map(phyml, file_paths)
    print("PhyML all finished!!!!!")
                            

def fasta2phy(file_paths):
    for file_path in file_paths:
        with open(file_path, 'r') as fin:
            sequences = [(m.group(1), ''.join(m.group(2).split()))
            for m in re.finditer(r'(?m)^>([^ \n]+)[^\n]*([^>]*)', fin.read())]
        with open(os.path.splitext(file_path)[0] + '.phy', 'w') as fout:
            fout.write('%d %d\n' % (len(sequences), len(sequences[0][1])))
            for item in sequences:
                fout.write('%-20s %s\n' % item)
    print("fasta file convert to phy file, all finished!")


def deletree_for_modelselect(file_paths):
    for file_path in file_paths:
        with open(file_path, 'r') as fin:
            phy_file = open(os.path.splitext(file_path)+'_sub.txt', 'w')
            phy_file.write(re.sub(r'\)[0-9]+:','):' , fin.readline())+'\n')
            phy_file.close()
    print("Substitued tree file!")
                            
def locarna(file_paths):
    for file_path in file_paths:
        try:
	    output_dir = os.path.splitext(file_path)[0]
            file_name = os.path.splitext(file_path)[0].split('/')[0]
	    ps = subprocess.Popen(["mlocarna",file_path,"--tgtdir",output_dir+"_results/","--write-structure"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	    output_lines = ps.stdout.readlines()
	    error_lines = ps.stderr.readlines()
	    f = open(output_dir+"_results/"+file_name+"_fold.txt","w")
	    for line in output_lines:
	        f.write(str(line,encoding = "utf-8"))
	        f.close()
	        f = open(output_dir+"_results/error_info.txt","w")
	    for line in error_lines:
	        f.write(str(line,encoding = "utf-8"))
	        f.close()

        except:
	    print("The file is wrong:"+input_file)
	    continue

    
def walkflow1():
    set_softwarePATH()

    main_path = get_dir_fullpath()
    print(main_path)
    files = get_files_fullPath(main_path, [".txt", ".fasta", ".fas"])                  
    print(files)
    siut_same_name_dir(files)
    files = get_files_fullPath(main_path, [".fasta",".txt", ".fas"])
    print(files)
    mclustalw(files)

    #
    aln_files = get_files_fullPath(main_path, ["_aln.fasta"])
    fasta2phy(aln_files)

    phy_files = get_file_fullpath(main_path, ["_aln.phy"])
    mphyml(phy_files)
    
def walkflow2():
    set_softwarePATH()

    main_path = get_dir_fullpath()
    files = get_files_fullPath(main_path, [".txt", ".fasta", ".fas"])
    siut_same_name_dir(files)
    files = get_files_fullPath(main_path, [".txt", ".fasta", ".fas"])

    locarna(files)

    files = get_files_fullPath(main_path, ["_fold.txt"])
    RNAalifold2fas_struct_rna(files)
    
    return
                    
if __name__ == "__main__":
    
    do = 1
    for do:
        print("Explain:\n\
        Usages: <workfolw>
        Workflow1,<flow1>:\n\
        0. Put the file 0f input under the directory of same name without file extersion.\n\
        1. Align degap file --> *_aln.fasta\n\
        2. Convert _aln.fasta to *_aln.phy (No limitation of 10 characters)\n\ 
        3. Build ML-tree using .phy format file\n\
        4. Finished, enjoy it!\n\
        
        Workflow2<flow2>:\n\
        0. As same as above.\n\
        1. Compute it using mlocarna of locarna.\n\
        2. Transform *_fold.txt to three files (.rna, .fa && .structure.txt).\n\
        3. Ended!\n")
        user_choiced = input("Please chose a workflow <workflow1 or workflow2>:\n").strip().strip('\'')
        if user_choiced == "workflow1":
            walkflow1()
            do = 0
        elif:
            walkflow2()
            do = 1
        else:
            continue
