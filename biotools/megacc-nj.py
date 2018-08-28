import subprocess
import multiprocessing
import os, re, sys

def get_dir_fullpath():
    return input("Please drog a dirctory to here:").strip().strip('\'')

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

def build_njtree(file_path):
    this_script_name = sys.argv[0]
    this_script_dir_name = os.path.dirname(this_script_name)
    subprocess.call(["megacc", "-a", this_script_dir_name + "\nj.mao", "-f", "Fasta", "-d", file_path,  "-o", os.path.splitext(file_path)[0]])


def mbuild_njtree(file_paths):
    pool = multiprocessing.Pool(processes=len(file_paths))
    pool.map(build_njtree, file_paths)
    
def workflow0():
    workdir = get_dir_fullpath()
    files = get_files_fullPath(workdir, [".txt", ".fasta", ".fas"])
    mbuild_njtree(files)

    
if __name__ == "__main__":
    do = 1
    while do:
        i = input("Please put in a choice:").strip().strip('\'')
        if i == "do" or "exit":
            do = 0
            
        else:
            continue
