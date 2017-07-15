![capitalize](doc/capitalize.png?raw=true  "capitalize")

## capitalize

### DESCRIPTION
    Capitalize a list of filenames based upon a set of command-line switches.


-----------------------------------------
#### author      : Chris Reid
#### category    : batch renaming
#### copyright   : Copyright 2015
#### country     : United States of America
#### credits     : [Python Software Foundation, Free Software Foundation ]
#### email       : spikeysnack@gmail.com
#### file        : capitalize
#### license     : Free for all non-commercial purposes. 
              Modifications allowed but original attribution must be included. 
              See (http://creativecommons.org/licenses/by-nc/4.0/)
#### maintainer  : chris Reid
#### modification_date : 10 Oct 2015
#### version     : 1.4
#### status      : Release Candidate
-----------------------------------------

### QUICK INSTALL:
      make
      sudo make install
The default installation is: 
    capitalize          /usr/local/bin
    capitalize.1        /usr/local/share/man/man1/capitalize.1
    
###EXPLANATION 

	Changing the case or capitalization of a group of files and/or directories
	is a chore and there are few straightforward ways to do it. Capitalize makes it quick and easy.    


    usage: *capitalize*  [options]  [file | file list]
           capitalize  -h 
   
           options:  
                    -f         --force         rename files without question (dangerous)
                    -h         --help          print this message
                    -i         --interactive   ask for each file before renaming
                    -l         --lower         uncapitalize all letters in filenames
                    -r         --recursive     recursively change all filenames in subdirectories
                    -t         --test          test mode -- do not actually change filenames 
                    -T         --Title         Capitalize with titlecase
                    -u         --upper         CAPITALIZE ALL LETTERS IN FILENAMES
                    -v         --verbose       print out lots of things as they happen 
           (hint:  use * for all files in dir)
## Example:  
	  Change all files to lower case.

	  $ capitalize  -l *
	  Fix bad capitalization.
	  $ 	  capitalize -Tvt THis\ FIle\ iS\ LEet.JPG 
	   TEST MODE    THis FIle iS LEet.JPG ==> This File Is Leet.jpg 	TEST MODE




  
