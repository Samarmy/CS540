I used a python script for this project. If you already know how to run a python script you can skip the set up paragraph below.

Set-Up:
If you are on a CSU CS department machine add the line:

export PATH=/usr/local/anaconda/bin:$PATH

to your .bashrc file in your home directory.

You may have to run:

source .bashrc 

for the changes to the .bashrc file to apply.

If you are on a non-CSU machine you need to install Anaconda which you can do at:

https://www.anaconda.com/distribution/#download-section

***Make sure you check mark the box that adds anaconda to your PATHs in the installer.

If you have any trouble with this, the jupyter notebook setup link is:

https://jupyter.readthedocs.io/en/latest/install.html
//////////////////////////////////////////////////////////////////////////////////////////////////////

After Set-Up:
In your terminal make sure you are in the directory with all my files.

If you want to add block world files you should add them in this directory.

Then in your terminal you can run the python script PA1.py by simply typing in:

python PA1.py <startState.txt> <goalState.txt>

It should print out the startState and a list of actions from the startState to the goalState followed by the total number of steps. 

If you want to change the startState or goalState you need to change the two input arguements after "python PA1.py " <startState.txt> <goalState.txt>