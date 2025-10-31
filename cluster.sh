#!/bin/bash
# Developed by Ruchan Yalçın
# ruchany13@gmail.com


current_path=$(pwd)
python3_path=$(which python3)

# ------ Help Function ---------#
Help()
{
   echo " script can up and down deployment, statefulset ,and daemonset on specific namespace"
   echo 
   echo "Syntax: scriptTemplate [up|down|setup|annotate]"
   echo "options:"
   echo "up <namespace>      Up cluster objects in namespace"
   echo "down <namespace>    Down cluster objects in namespace"
   echo "setup               install python requirements"
   echo "annotate            run order.txt for annotate order to kubernetes object"
   echo 
}
#-----------------------------#


if [ $1 == "up" ]; then
$python3_path Python/up_cluster.py $2

elif [ $1 == "down" ]; then
$python3_path Python/down_cluster.py $2

elif [ $1 == "setup" ]; then
pip install -r requirements.txt &> setup.log ||  pip install -r requirements.txt --break-system-packages &> setup.log
echo "Setup is complete 
Log file is $current_path/Python/setup.log"

elif [ $1 == "annotate" ]; then
. order.txt

else
Help

fi