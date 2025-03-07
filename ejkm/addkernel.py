import os
import argparse
import json

##########################
### test codes (examples)
### python addkernel.py --img quantum-mobile_20_11_2a.sif
### python addkernel.py --img docker://python
### python addkernel.py --img "quantum-mobile_20_11_2a.sif" --kpath "/usr/bin/python3" --dname "py3 (qe-singularity)"
### python addkernel.py --img "quantum-mobile_20_11_2a.sif" --scanonly yes
### python addkernel.py --rmall yes
##########################

def getUserID():
    import subprocess
    with subprocess.Popen(['whoami'], stdout=subprocess.PIPE) as proc:
        res=proc.stdout.read().decode("utf-8").strip('\n')
        return res

def getUserHomeDir():
    return os.path.expanduser('~')    
    
def getsimgLoc(simg_name):
    if "docker://" in simg_name.lower():
        res = autoBuildSingularityImagefromDockerRepository(simg_name) # sandbox will be supported 20230816
    else:
        res = os.path.join(os.getcwd(),simg_name)
    return os.path.abspath(res)

def autoBuildSingularityImagefromDockerRepository(simg_name):
    import subprocess
    sif_name=os.path.basename(simg_name)+'.sif'
    command = ['singularity',
               'build',
               sif_name,
               simg_name
              ]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
        res=proc.stdout.read().decode("utf-8")
    return os.path.join(os.getcwd(),sif_name)

def getkernelDictandgenJSON(args, simgLocAbsolutePath, kpath):
    res = {}
    res.update({"language":"python"})
    singularity_dict=["singularity", "exec","--writable-tmpfs", simgLocAbsolutePath, kpath, "-m", "ipykernel", "-f", "{connection_file}"]    
    ########
    res.update({"argv":singularity_dict})
    res.update({"display_name":args.dname})
    env_dict={}
    if "python" in kpath:
        env_dict.update({"pip":kpath+" -m pip"})
    res.update({"env":env_dict})
    kernelJsonGen(args, res, kpath)

def autogetkernelDicts(args, scanonly):
    simgLocAbsolutePath = getsimgLoc(args.img) #including instant building
    if os.path.exists(simgLocAbsolutePath):
        if args.kpath == 'auto':
            kpath_list = autogetPythonKernels(simgLocAbsolutePath) 
            if len(kpath_list)==0:
                print("error: there is no python kernel in this image. Try another image.")
                exit(-1)
            if scanonly=="yes":
                print(kpath_list)
                exit(-1)
            for each in kpath_list:
                getkernelDictandgenJSON(args, simgLocAbsolutePath, each)
        else:
            getkernelDictandgenJSON(args, simgLocAbsolutePath, args.kpath)
    else:
        print("error: singularity image ("+simgLocAbsolutePath+") not founded.")
        exit(-1)          
        
def kernelJsonGen(args, res_dict, kpath):
    user = getUserID() # kisti
    user_home = getUserHomeDir()
    img_name = os.path.basename(args.img)#"quantum-mobile_20_11_2a"
    kernel_name = kpath.replace("/","_")
    kernelAdding(user_home, img_name, kernel_name, args, kpath, res_dict)

def kernelAdding(user_home, img_name, kernel_name, args, kpath, res_dict):
    #### check 1 local
    locald = os.path.join(user_home, ".local")
    if os.path.exists(locald):
        print("we have .local/")
    else:
        print("mkdir .local/")
        os.mkdir(locald)
    ##### check 2 share
    locald_with_share = os.path.join(locald, "share")
    if os.path.exists(locald_with_share):
        print("we have share/")
    else:
        print("mkdir share/")
        os.mkdir(locald_with_share)
    ##### check 3 jupyter
    locald_with_share_jupyter=os.path.join(locald_with_share,"jupyter")
    if os.path.exists(locald_with_share_jupyter):
        print("we have jupyter/")
    else:
        print("mkdir jupyter/")
        os.mkdir(locald_with_share_jupyter)
    ##### check 4 kernels
    locald_with_share_jupyter_kernels=os.path.join(locald_with_share_jupyter,"kernels")
    if os.path.exists(locald_with_share_jupyter_kernels):
        print("we have kernels/")
    else:
        print("mkdir kernels/")
        os.mkdir(locald_with_share_jupyter_kernels)
    ##### check 5 img_name
    img_name = "CUSTOM__"+img_name
    locald_with_share_jupyter_kernels_imgname = os.path.join(locald_with_share_jupyter_kernels, img_name)
    locald_with_share_jupyter_kernels_imgname_kernelname = locald_with_share_jupyter_kernels_imgname+"__"+kernel_name
    if os.path.exists(locald_with_share_jupyter_kernels_imgname_kernelname):
        print("we have "+img_name+"__"+kernel_name)
    else:
        print("mkdir "+img_name+"__"+kernel_name)
        os.mkdir(locald_with_share_jupyter_kernels_imgname_kernelname)
    #
    file_path = os.path.join(locald_with_share_jupyter_kernels_imgname_kernelname,"kernel.json")
    if args.dname == 'auto':
        res_dict.update({'display_name':os.path.basename(locald_with_share_jupyter_kernels_imgname_kernelname)})
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(res_dict, file)
    print("JSON(kernel conf.) has been generated successfully.")
    if "python" in kpath:
        os.system("singularity exec "+getsimgLoc(args.img)+" "+kpath+" -m pip install ipykernel")

def autogetPythonKernels(absolute_singularity_image_filepath):
    ### find python?.? or python?.?? (number) executable paths in the singularity container image
    import subprocess
    args='''singularity exec python.sif bash -c'''
    command = ['singularity',
               'exec',
               absolute_singularity_image_filepath,
               'bash',
               '-c',
               "find / ! \( -type d -path '*python[[:digit:]].[[:digit:]]*' -prune \) -executable -name '*python[[:digit:]].[[:digit:]]' -o -name '*python[[:digit:]].[[:digit:]][[:digit:]]' 2>/dev/null | grep bin/",
              ]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
        res=proc.stdout.read().decode("utf-8")
        return [res for res in res.split('\n') if res]        
        
def removeAllCustomKernels():
    import os,glob, shutil
    dirlist = glob.glob(os.path.join(os.path.join(getUserHomeDir(),'.local/share/jupyter/kernels/CUSTOM__*')))
    for each in dirlist:
        try:
            shutil.rmtree(each)
        except OSError:
            os.remove(each)
    print("REMOVE CUSTOM kernels successfully.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="EDISON Jupyter Kernel Management Program")
    parser.add_argument('--img', help="filepath of the singularity container, e.g., /home/kisti/qm.sif or docker://python3 (docker image will be build into /{pwd}/{docker_name}.sif)")
    parser.add_argument('--kpath', help="specific python kernel path in the container, default is 'auto'", default='auto')#, e.g., "/usr/bin/python"
    parser.add_argument('--dname', help="specific python kernel display name in jupyter, default is 'auto'", default='auto')#, e.g., "Python3 (qe-singularity)"
    parser.add_argument('--scanonly', help="scan python kernel path only in a specific container (yes/no), default is 'no'", default="no")
    parser.add_argument('--rmall', help="remove all custom kernels (yes/no), default is 'no'", default="no")
    # 인자가 없는 경우 기본 도움말을 표시합니다.
    args = parser.parse_args()
    # 사용자가 아무런 인자도 제공하지 않았을 때 도움말을 표시하도록 설정합니다.
    if not any(vars(args).values()):
        parser.print_help()
        return
    args=parser.parse_args()
    if args.rmall=='yes':
        removeAllCustomKernels()
    else:
        if (args.img is None) or (args.img==""):
            print("error: please input singularity container image path or docker address by using --img option.")
            exit(-1)
        else:
            autogetkernelDicts(args, args.scanonly)

    
if __name__ == "__main__":
    main()
