# EDISON Jupyter Kernel Management
**Binding Python kernels in a container image to a Custom User Interactive Development Enviroment (IDE) at Jupyter Notebook**

## Steps
`
1. Build a singularity container image from a docker repository such as DockerHub
2. Discover python kernels in the container image
3. Bind kernels into jupyter notebook interface
`

## Image Build Location Example : {user_home}/.singularity/{image_name}.sif 

## Test Codes (examples)
`
ejkm --img quantum-mobile_20_11_2a.sif
ejkm --img "quantum-mobile_20_11_2a.sif" --kpath "/usr/bin/python3" --dname "py3 (qe-singularity)"
ejkm --img "quantum-mobile_20_11_2a.sif" --scanonly yes
ejkm --rmall yes
`

## Installation
`pip install git+https://github.com/jclee0333/ejkm.git`
