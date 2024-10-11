# EDISON Jupyter Kernel Management
**Binding Python kernels in a container image to a Custom User Interactive Development Enviroment (IDE) at Jupyter Notebook**

## Steps
```
1. Build a singularity container image from a docker repository such as DockerHub
2. Discover python kernels in the container image
3. Bind kernels into jupyter notebook interface
```

## Image Build Location Example : {user_home}/.singularity/{image_name}.sif 

## Usage
```
usage: ejkm [-h] [--img IMG] [--kpath KPATH] [--dname DNAME] [--scanonly SCANONLY] [--rmall RMALL]

EDISON Jupyter Kernel Management Program

optional arguments:
  -h, --help           show this help message and exit
  --img IMG            filepath of the singularity container, e.g., /home/kisti/qm.sif or docker://python3
                       (docker image will be build into /{pwd}/{docker_name}.sif)
  --kpath KPATH        specific python kernel path in the container, default is 'auto'
  --dname DNAME        specific python kernel display name in jupyter, default is 'auto'
  --scanonly SCANONLY  scan python kernel path only in a specific container (yes/no), default is 'no'
  --rmall RMALL        remove all custom kernels (yes/no), default is 'no'
```

## Test Codes (examples)
```
ejkm --img quantum-mobile_20_11_2a.sif
ejkm --img "quantum-mobile_20_11_2a.sif" --kpath "/usr/bin/python3" --dname "py3 (qe-singularity)"
ejkm --img "quantum-mobile_20_11_2a.sif" --scanonly yes
ejkm --rmall yes
```

## Installation
`pip install git+https://github.com/jclee0333/ejkm.git`

## License
MIT License

## Korea Institute of Science Technology and Information (KISTI)
