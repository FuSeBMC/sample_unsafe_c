#!/bin/bash

# Define variables
REPO_URL="git@github.com:kaled-alshmrany/FuSeBMC-UoM.git"
REPO_NAME="fusebmc"

echo "cloning FuSeBMC"
git clone "$REPO_URL" "$REPO_NAME" || echo "FuSeBMC already cloned, continue"

if [ $? -ne 0 ]; then
    echo "Failed to clone FuSeBMC"
    exit 1
fi

git fetch

echo "checkout imago_testing branch" 
cd "$REPO_NAME" || { echo "Error: Failed to change directory to $REPO_NAME"; exit 1; }

git switch "imago_testing" || echo "Already on imago_testing branch, continue"


echo "running FuSeBMC : './fusebmc.py -a 64 -s incr -p properties/valid-memsafety.prp ../unsafe.c'"

./fusebmc.py -a 64 -s incr -p properties/valid-memsafety.prp ../unsafe.c


echo "running FuSeBMC : './fusebmc.py -a 64 -s incr -p properties/coverage-error-call.prp ../unsafe.c'"

./fusebmc.py -a 64 -s incr -p properties/coverage-error-call.prp ../unsafe.c


