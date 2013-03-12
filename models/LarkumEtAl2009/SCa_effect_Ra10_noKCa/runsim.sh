#!/bin/bash -l

# Local simfolder
cd /Users/danielruedt/PhD/simulations/model_validation/800_4Hz_dt0.1/

# Simulation reference
export simRef="800_4Hz_dt0.1"
export projName="LarkumEtAl2009_local"

export remoteHost="128.16.14.177"
export remoteUser="ucbtdcr"
export simulatorLocation="/share/apps/neuro/nrn71/x86_64/bin/nrniv"

# Sim path on the cluster
projDir=/home/ucbtdcr/simulations/model_validation/
simDir=$projDir$simRef

echo "Going to send files to dir: "$simDir" on "$remoteHost
echo "Local dir: "$PWD

echo "cd $simDir;/opt/SUNWhpc/HPC8.2.1/gnu/bin/mpirun --mca btl openib,self -host  node0 "$simulatorLocation" -mpi  "$simDir"/"$projName".hoc">runmpi.sh

chmod u+x runmpi.sh

ssh $remoteUser@$remoteHost "mkdir $projDir"
ssh $remoteUser@$remoteHost "rm -rf $simDir"
ssh $remoteUser@$remoteHost "mkdir $simDir"

zipFile=$simRef".tar.gz"

echo "Going to zip files into "$zipFile

tar czvf $zipFile *.mod *.hoc *.p *.g *.props *.dat *.sh *.py *.xml *.h5 *Utils *.cll

echo "Going to send to: $simDir on $remoteUser@$remoteHost"
scp $zipFile $remoteUser@$remoteHost:$simDir

ssh $remoteUser@$remoteHost "cd $simDir;tar xzf $zipFile; rm $zipFile"
# ssh $remoteUser@$remoteHost "cd $simDir;/bin/bash -ic /share/apps/neuro/nrn71/x86_64/bin/nrnivmodl" # Now run on compute node
ssh $remoteUser@$remoteHost "cd $simDir;/bin/bash -ic 'qsub subjob.sh'"
ssh $remoteUser@$remoteHost "echo 'Submitted job!';/bin/bash -ic 'qstat -u $remoteUser'"
rm -rf $zipFile
sleep 2


rm checkingRemote

