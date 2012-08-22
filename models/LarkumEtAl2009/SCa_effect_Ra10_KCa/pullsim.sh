#!/bin/bash 


export simRef="800_4Hz_dt0.1"
export projName="LarkumEtAl2009_local"

export targetDir="/home/ucbtdcr/simulations/model_validation/"
export remoteHost="128.16.14.177"
export remoteUser="ucbtdcr"


projDir=/home/ucbtdcr/simulations/model_validation/
simDir=$projDir$simRef

export localDir=/Users/danielruedt/PhD/simulations/model_validation"/"$simRef"/"

remoteTimeFile=$simDir"/time.dat"
localTimeFile=$localDir"time.dat_temp"
scp $remoteUser@$remoteHost:$remoteTimeFile $localTimeFile
if [ -e $localTimeFile ] 
then

rm $localTimeFile

checkingRemoteFile=$localDir"checkingRemote"

echo "Temporary file indicating check is in progress...">$checkingRemoteFile


echo "Going to get files from dir: "$simDir" on "$remoteHost" and place them locally on "$localDir

zipFile=$simRef".tar.gz"

echo "Going to zip files into "$zipFile

ssh $remoteUser@$remoteHost "cd $simDir;tar czvf $zipFile *.dat *.h5 *.props *.spike log*"

cd $localDir
scp $remoteUser@$remoteHost:$simDir"/"$zipFile $localDir

tar xzf $zipFile
rm $zipFile
ssh $remoteUser@$remoteHost "cd $simDir;rm $zipFile"
rm $checkingRemoteFile

else
echo "Simulation not finished yet..."
fi
