#!/usr/bin/env sh


RESPONSE="Y\nY\nN\nY\nN\nY\nN\n"
DIRLIST="ls --format=vertical -R -w 40"


# show dir with lines
dir_list()
{
echo "-----------------------------------"
$DIRLIST
echo "-----------------------------------"
}

make_dirs()
{
C_DIR="$(pwd)"
rm -rf  test
mkdir -p "test/level1/level2/level3"
cd test
touch Ant  Bagel  Cat  Dog  Eagle  "Some Long Thing" 
cd level1
touch Food.txt  Insect Mammal
cd level2
touch Bat  Bird  Snake
cd level3
touch Cow  Llama  Zebra
cd "${C_DIR}"
}


make_dirs

cd test

echo "[TEST CAPITALIZE]"

../capitalize.py -v -u *

dir_list

echo "[interactive (lowercase)]"
#echo -e "${RESPONSE}" | ../capitalize  -r -l -i * 
../capitalize.py  -l -i * 

dir_list



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# emacs               #
# Local Variables:    #
# mode: shell-script  #
# mode: font-lock     #
# tab-width:8         #
# End:                #






   

  
