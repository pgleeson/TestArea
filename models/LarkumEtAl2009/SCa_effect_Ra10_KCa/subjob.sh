#!/bin/bash -l

#$ -l  vf=2G
#$ -l  h_vmem=2G
#$ -l  h_rt=36:0:0

#$ -wd  /home/ucbtdcr/simulations/model_validation/800_4Hz_dt0.1/
#$ -o  /home/ucbtdcr/simulations/model_validation/800_4Hz_dt0.1/log
#$ -j y
#$ -N  800_4Hz_dt0.01_LarkumEtAl2009_local

#$ -l fc=yes
#$ -R y
#$ -pe smp  1

/bin/bash -ic '/share/apps/neuro/nrn71/x86_64/bin/nrnivmodl'
/bin/bash -ic '/opt/SUNWhpc/HPC8.2.1/gnu/bin/mpirun --mca btl openib,self -np $NSLOTS /share/apps/neuro/nrn71/x86_64/bin/nrniv -mpi /home/ucbtdcr/simulations/model_validation/800_4Hz_dt0.1/LarkumEtAl2009_local.hoc'

