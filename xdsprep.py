"""

This is a script to (hopefully) unpack all tar files in folders after 
crystallography collection, then make a directory in each new folder, copy the 
"filename"_XDS.INP to the new folder new name as XDS.INP. Will update later to 
change the necessary lines in the XDS.INP and run all the xds commands. 

                    First Working Version: 08/15/15
Works well enough, but with only one problem. Every file that ended in "_1" it
works perfectly: Moves, untars, moves into new directory, makes new directory, 
copies .INP file to analysis folder and renames it "XDS.INP". Flaw comes in with 
a file called "C9_8_C3_2". The untarred folder adds a "_2" instead of the "_1"
it makes with the others. Idea: Sparse the folder name use the last piece of string as a variable and then
put that as the "_x" end?

Created by Patrick O'Brien
August 14, 2015

"""




import os
import sys
import tarfile
import shutil 


master = os.getcwd(); 
print master; 

for folder in os.listdir(master):
    if str(folder) == '.DS_Store': #This is needed in OS X due its addition
        print "skip this Mac OSX addition" # It can be seem with "ls -a" 
    else:                                  # I didn't want to delete it worked around it and added the if/else loop.
        print folder;          #keeps track of where it is            
        os.chdir("%s/%s" % (master, folder)); # moves into the dir with tarball
        # print os.getcwd();       #this line was used to make sure in right place in development             
        tar = tarfile.open('%s_1.tar.bz2' % folder);
        tar.extractall() 
        cwd = os.getcwd(); 
        os.chdir('%s/%s_1' % (cwd, folder)); 
        cwd = os.getcwd(); 
        os.mkdir('%s/analysis' % cwd); 
        shutil.copy(('%s_1_XDS.INP' % folder), ('%s/analysis/XDS.INP' %cwd)) 
        os.chdir('%s' % master); 
        print "%s is done" % folder; 
