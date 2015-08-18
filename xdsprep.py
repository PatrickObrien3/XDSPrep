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
it makes with the others. Idea: Sparse the folder name use the last piece of 
string as a variable and thenput that as the "_x" end?

                    Second Working Version: 08/17/15
                    
Now works with all file names. Worked around not having the specific name by 
making a list of the contents of the directory, where the first listing will 
always be the new folder. Calling both[0] gives a string of the folder that was 
created, and using a modulus s in the os.chdir command allowed for it to be 
recognized and change. 

                     Third Working Version(First of runxds.py): 08/18/15
                    
Have now made a function that imports the XDS.INP file, writes the contents to 
a list, then replaces the JOB, # of processors, Resolution range, and Friedels's 
law variables from user input (except for JOB which changes the default value to
ALL). Also have functionality replacing the file path with user-inputed file 
path to the runs directory.However, there is a small bug where for some reason 
it puts two copies of the NAME_TEMPLATE_OF_DATA_FRAMES=..... line.. The code 
still runs with no problems though.The next task will be incorporating this 
function into the overall xdsprep.py file. 


                      Fourth Working Version: 08/18/15

This version incorporates both xdsprep and xdsrun in one file. Note: There are 
three ways to run this script.

1.  Subprocess.check_call('xds') is at the end of each xdsprep function. This 
    will do the xds step inbetween each folder. Convenient if you have a large 
    number of data sets and don't mind waiting. 
    
2.  The second doesn't use the subprocess.check_all('xds') to start the xds 
    processing. This version is easily gotten from this version by simply 
    commenting out the subprocess.check_all('xds') line at the end of the 
    xdsprep function. This could be better if you wanted to start processing 
    multiple files at once and manually would run xds once the individual 
    folders were set up.

3.  A third option is the reset the file to be able to call the entire script on 
    just one folder at a time, with the subprocess.check_all('xds') included. 
    This would include using as many python windows as you have folders, and I'm 
    not sure if it would kill your performance. Also, this would be costly from
    a standpoint of having to enter the path, Friedels preference, resolution 
    limits, and number of processors that many times. They could be set manually
    and not be raw_input variables and that would help make the set up much
    more efficient. Note: Have not made this file yet. 
    

                        Created by Patrick O'Brien
                              August 14, 2015

"""



import subprocess, os, tarfile, shutil, fnmatch


master = os.getcwd(); 
print master; # This will be used to start back at the original spot and is
              # and is never re-set during the script


################################################################################
################################################################################
################################################################################

"""
                            User Input for the XDS.INP File
                            
The following section is used to change the default variables in the xds.inp 
file. These are prompts that the person must enter, and instructions are 
provided so as to minimize confusion.

"""

# Input for setting the path to images.

print """
Please enter the full path to the directory 
containing the image folders. This should
look like:  /Users/name/Desktop/images/name/runs/

NOTE: Path MUST start and end with '/' 
"""
beginp = raw_input("Path: ")

# Input for setting Friedel's law to TRUE

print """
\nDo you want Friedels Law to be TRUE or FALSE? 
Enter your choice in all capital letters please.\n'
"""
friedel = raw_input("TRUE or FALSE: ")

# Input for changing the resolution evaluated

print """
The next two questions relate to the resolution 
range for the initial processing run.
First, what would you like the upper 
range (in Angstroms) to be? (Default is 200.0)\n
"""
uprange = raw_input("Upper Range: ")

print '\nSecond, what would you like the lower range to be? (Default is 0.0)\n'
lowrange = raw_input("Lower Range: ");

# Set the resolution replacement string
bothr = '%s %s' % (uprange, lowrange);

# Input for setting the maximum number of processors

print '\nWhat is the maximum number of processors? (Default is 8)';
processors = raw_input("Number of Processors: ");

# Since this is the initial xds run there is no option to specify the 
# setting for JOB, but this could be changed in similar ways to the others

print '\nNote, this script changes the default JOB to ALL\n' 

# This just repeats what was done for a brief summary. 

print '-' * 10; 
print """
\n This will generate your XDS.INP file with the following settings: 
\t Path to images: %s 
\t Friedels law set to: %s
\t Number of processors set to: %s
\t Upper Resolution limit: %s
\t Lower Resolution limit: %s
\t JOB set to: ALL 
""" % (beginp, friedel, processors, uprange, lowrange);
print '-' * 10; 


################################################################################
################################################################################
################################################################################

"""

Below is the runxds function. It is different than the original file in that
the instead of runxds() it is now runxds(filename) so that it can be run easily 
in the xdsprep function (further below). 
               
               
"""                         
        
        
def runxds(filename):
    fr = open(filename);
    lines = fr.readlines();
    #print lines; # Used to check and make sure everything was there
    fr.close();
    
    # Here we set up the path; messy way to do it but if its all on the
    # same line in every file it works. 
    l = lines[6].split('/');
    endp = l[-2] + '/' + l[-1];
    imagepath = beginp + endp;
    name = l[0];
    frames = name + imagepath;
    #print frames; # Used in dev. 
    
    fw = open(filename, 'w'); 
    for line in lines:
        if "DATA_FRAMES" in line:
            line = line.replace(line, frames);
            print line;
            fw.write(line);
             
        if 'FRIEDEL' in line:
            line = line.replace('FALSE', friedel); 
            fw.write(line);
            
        elif 'JOB' in line:
            line = line.replace('INTEGRATE CORRECT', 'ALL'); 
            fw.write(line);
            
        elif 'MAXIMUM_NUMBER' in line:
            line = line.replace('8', processors); 
            fw.write(line);
            
        elif 'INCLUDE_RESOLUTION' in line:
            line = line.replace('200.0 0.0', bothr);
            fw.write(line);
        else:
            fw.write(line);
    fw.close();
    
    
################################################################################
################################################################################
################################################################################

"""

                            xdsprep Function

Below is the xdsprep function. It is called by opening the python file in the 
directory with the folders that the analysis is going to be one. 

"""

def xdsprep(folder):
    

    if str(folder) == '.DS_Store': #This is needed in OS X due its addition
        print "skip this Mac OSX addition" # It can be seem with "ls -a" 
    else:                                  # I didn't want to delete it worked 
        print folder;                      # around it and added the elif loop          
        os.chdir("%s/%s" % (master, folder)); # moves into the dir with tarball
        # print os.getcwd(); # used in dev            
        pattern = '*.bz2';
        files = os.listdir('.');
        print 'pattern: ', pattern;
        print 'files : ', files; 
        tarball = fnmatch.filter(files, pattern);
        splitname = tarball[0].split('.')
        exname = splitname[0]
        print "extended filename is: ", exname
        print "The tarball is: ", tarball
        tar = tarfile.open(tarball[0]); #try this; might have to use modulus..
        tar.extractall() 

        cwd = os.getcwd(); 
        # the both variable below is not needed anymore. 
        #both = os.listdir('.'); 
        os.chdir('%s/%s' % (cwd, exname)); 
        cwd = os.getcwd(); 
        os.mkdir('%s/analysis' % cwd); 
        shutil.copy(('%s_XDS.INP' % exname), ('%s/analysis/XDS.INP' %cwd)) 
        
        # Now going to set the correct variables in the XDS.INP file
        
        os.chdir('%s/analysis' % cwd);
        runxds('XDS.INP');
        
        # Here the xds process is called
        subprocess.check_call('xds')
        
        os.chdir(master); 
        
        #the "\a" in the print command below sounds off a bell when the 
        # script is done.
        
        print "%s is done \a" % folder; 

################################################################################
################################################################################
################################################################################
       
# Here the function is actually called for the folder.                      
# Recall master = os.getcwd() and was run at the very beginning of the file.
      
for folder in os.listdir(master):
    xdsprep(folder);

    
         
        
        

