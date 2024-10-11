# EDISON Jupyter Kernel Management
**Web Application to link Python kernels in a container image to a Custom User Interactive Development Enviroment (IDE) at Jupyter Notebook**

## Image Build Location Example : {user_home}/.singularity/{image_name}.sif 

## Test Codes (examples)
## ejkm --img quantum-mobile_20_11_2a.sif
## ejkm --img "quantum-mobile_20_11_2a.sif" --kpath "/usr/bin/python3" --dname "py3 (qe-singularity)"
## ejkm --img "quantum-mobile_20_11_2a.sif" --scanonly yes
## ejkm --rmall yes

## Installation
`pip install git+https://github.com/jclee0333/ejkm.git`
