#!/usr/bin/env python
# -*- coding: utf-8 -*-

# capitalize

""" capitalize
    Rename a list of filenames 
    to capitalizes, lowercase, 
    titlecase, or uppercase.

""" 

#-----------------------------------------
__author__      = "Chris Reid"

__category__    = "batch renaming"

__copyright__   = "Copyright 2016"

__country__     = "United States of America"

__credits__     = ["Python Software Foundation", "Free Software Foundation" ]  

__email__       = "spikeysnack@gmail.com"

__file__        = ["capitalize" , "capitalize.py"]

__license__     = """Free for all non-commercial purposes. 
                  Modifications allowed but original attribution must be included. 
                  see (http://creativecommons.org/licenses/by-nc/4.0/)"""

__maintainer__  = "chris Reid"

__modification_date__ = "7 Feb 2016"

__version__     = "1.2"

__status__      = "Issue Candidate 1"


#-------------------
# config options
config = {

  "options": {

    "short": "fhiulrtTv" ,

    "long": [ "force", "help" , "interactive", "upper", "lower", "recursive", "test", "Title", "verbose" ]
  }

} # config
""" dictionary: short and long command line options """

#--------
# globals


Debug       = False 
#Debug       = True 
force       = False
verbose     = False
interactive = False
test        = False
recursive   = False  



global_options = {
  "force"       : False,
  "Debug"       : False,
  "verbose"     : False,   
  "interactive" : False,
  "test"        : False,
  "recursive"   : False
}
""" dictionary: global boolean options  ( not yet used )"""

#-----------------
# python libraries

  
import os
import sys
import getopt 
import string

#----------------
# print to stderr
def eprint(*args):
  sys.stderr.write(' '.join(map(str,args)) + '\n')

def debug( s ):
  if Debug: 
    eprint("[Debug]:\t" + s)



__all__ = [ "renameError", "safe_rename", "rename" , "yesno", "parse_args" ]



#----------------------------
class renameError(Exception):

  """ an Exception class just for renaming errors 
  
  Parent Class:
  Exception  (built-in)
  
  Args:
  value(object): a string-convertable object
  
  """
  
  def __init__(self, value):
    """ initializer sets the value contained in the error (ususally string)"""
    self.value = value

  def __str__(self):
    """ helps convert value to string 
      
    Returns:
            a string representation of value
    """
    return repr(self.value)


#-----------------------------------
def safe_rename( oldname , newname):

  """ rename a file but make sure
      not to destroy an already existing one
      with different capitalization.
  
  Args:
       oldname(string): the original filename
       newname(string): the new proposed filename
  
  Raises: 
      renameError: the file exists and is not forced

  Note:
      Exits the program with a message. 
   
  """
  dirstr = ""

  if oldname == newname:    
    debug("[safe_rename] OLDNAME = NEWNAME" )
    pass
  else:

    try:
      
      debug( "[safe_rename]( " + oldname + " , " + newname + " )" )
      
      if os.path.exists( newname ):

        if os.path.isdir(newname):
          raise OSError("dir exists -- no rename")

        if (not force) :
          raise renameError( newname )

      else:
        if os.path.isdir(oldname):
          dirstr = "\t[DIR]"

        if verbose:
          what = oldname + " ==> " + newname + dirstr  
          print ( (what.center(60 ,' ' )) )

        os.rename( oldname, newname ) # this is the only actual potentially destructive op
      
    except renameError as rne:
      debug ( rne.value + " already exists. Not renaming " + oldname  + ".")

      if yesno("continue renaming other files?"):
        pass
      else:
        sys.exit(2)
    except OSError as ose:
      debug( "OSError: " + str(ose) )
      pass


#---------------------------
def rename( action, fn ):

  """ takes a command and a file name and returns the appropriately changed file name. 

  Args:
       action(string): what action to take

       fn(string):     a file name

  """

  rf = None


  dtable = {
    "upper": str.upper,
    "lower": str.lower, 
    "title": str.title,
    "capitalize": string.capwords
  }

  """ dictionary: a dispatch table of commands(string) and  functions(callable) to execute """
  
  debug("[rename] " +  action + " " + fn) 

  if test:
    newname = dtable[action](fn)
    what = fn + " ==> " + newname 
    print( ("TEST MODE\t" + what.center(60, ' ')  + "\tTEST MODE") )

  # renames all subfolders of dir, not including dir itself
  def rename_all( root, items):

    """ an internal function for recursive renaming """

    for name in items:
      try:

        debug ("[rename_all] " + name ) 

        newname = dtable[action](name)

        if name == newname:
          continue

        if not test:
          if interactive and yesno( "rename " + name + " => " + newname +  "?" ): 
            safe_rename( os.path.join(root, name), os.path.join(root,  newname ))
          elif not interactive:
            safe_rename( os.path.join(root, name), os.path.join(root,  newname ))          

      except OSError:
        pass # can't rename it, so what



  if os.path.isdir(fn):
    debug("ISDIR ------------------------" + fn) 

    newname = dtable[action](fn)
     
    if recursive:
      for root, dirs, files in os.walk( fn, topdown=False ):


        debug("root:\t" + str(root) + "\tdirs:\t" + str(dirs) + "\tfiles:\t" + str(files))

        if not test:
          rename_all( root, files)
          rename_all( root, dirs )

      safe_rename( fn, newname )

    else:
      debug("[not recursive]")

      newname = dtable[action](fn)

      if fn == newname:
        pass

      if not test:
        if interactive and yesno( "rename " + fn + " => " + newname +  "?" ):  
          safe_rename( fn, newname )
        else:
          safe_rename( fn, newname )    

    debug("ISDIR ------------------------" + fn )
 
  elif os.path.isfile(fn) or os.path.islink(fn):
    try:


      debug( "isfile(fn) or islink(fn)" )

      newname = dtable[action](fn)

      if fn == newname:
        raise  ValueError()

      if not test:
        if interactive and yesno( "rename " + fn + " => " + newname +  "?" ):  
          safe_rename( fn, dtable[action](fn) )
        else:
          safe_rename( fn, dtable[action](fn) )

    except ValueError:
      pass
    except OSError:
      pass
  else:
    pass


#-----------
def usage():

    """ print out a usage message """

    utext = '''\
    usage: capitalize  [options]  [file | file list]
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
    '''

    eprint (utext)

    if os.geteuid() == 0:  # remind superuser of danger
        eprint ("WARNING -- renaming system files could make your system unusable or even prevent booting!")


#-------------
def parse_args(argv):                         

    """ Parse the commandline and return opts separated from args. 
    
        Args:

            argv (object): all the command line options and args (sys.argv)

        Returns:

            arglen (int): the length of the arguments (without the options)

            args  (list): match, replacement, and files to consider

            flags (list): list of pairs (name:val) of options 
           
    """

    args    = []
    """list: a list of (str) arguments ( 1 match, 1 replacement, (list) filenames ) """ 

    arglen  =  0
    """int: how many arguments. """

    flags   = []
    """list: a list of (str:str) pairs of the option flags and option arguments 
           Example:
                [ ('title' ,'') , ('test', ''), ('interactive', '') ]
    """

    opts    = []
    """list: a list of pairs (str:str).  option flags and option arguments. 
           Example:
                [ ('-v' ,'') , ('--test', ''),('--interactive', '') ]
                [ ('-h','')]

    """


    # get and validate commandline options and arguments, parse them into separate lists
    # exit on bad options
    try:                                

        opts, args = getopt.getopt(argv, config["options"]["short"], config["options"]["long"] ) 

        arglen = len(args)

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if not opts:
        # print ("NO OPTIONS" )
        arglen = len(argv)
        args = argv
        flags = ""
        return arglen, args, flags

#    "options": {
#        "short": "hiultTv" ,
#        "long": [ "help" , "interactive", "upper", "lower", "test", "Title", "verbose" ]

    # check the arguments
    for opt, optarg in opts:

        if opt in ('-h', "--help"):
            flags.append( ("help",'') )

        elif opt in ('-f', "--force"):
            flags.append( ("force",'') )

        elif opt in ('-i', "--interactive"):
            flags.append( ("interactive",'') )

        elif opt in ( "-orw", "--override-root-warning" ):  
            flags.append( ("override_root_warning", '') )
 
        elif opt in ('-l', "--lower"):
            flags.append( ("lower",'') ) 

        elif opt in ('-r', "--recursive"):
            flags.append( ("recursive",'') )

        elif opt in ('-t', "--test"):
            flags.append( ("test",'') ) 

        elif opt in ('-T', "--Title"):
            flags.append( ("Titlecase", '') )

        elif opt in ('-u', "--upper"):
            flags.append( ("upper",'') ) 

        elif opt in ('-v', "--verbose"):
            flags.append( ("verbose",'') )  

    return arglen, args, flags  



#--------------------
def yesno(ask = '' ):

    """ Gets yes or no from the user. 
    
    Args:
        
        ask (str): a question prompt

    Returns:
       
        bool: True if Yes or [return] , False  if no

    Note:

       repeats until it gets a valid response

    """
    #python 2 vs python 3
    try:
      line_input = raw_input
    except NameError:
      line_input = input
          

    yes = set(['yes','y', 'ye', '']) # [return] = yes
    no = set(['no','n'])

    if ask:
        print( ask ) 

    choice = line_input().lower()

    while choice not in yes|no:
        print("What? please answer y or n or [return=yes]")
        choice = line_input().lower()

    if choice in yes:
        return True
    elif choice in no:
        return False




if __name__ == '__main__':

    """ executes if called as a program 
    
    Args:
    
    sys.argv (object): command line arguments object of sys lib
    
    Returns:
    
    (int): exit code through python interpreter and up to shell
    0   for no errors
    -1  for bad file names
    2   for wrong number of arguments  
    
    
    Raises:
    
    OSError: if filename change fails
    
    """    
    args        = []
    """list: only the arguments, not the options"""

    dups        = []
    """list: duplicate filenames (bad)"""

    flags       = []
    """list: list of (option:val) pairs """

    numargs     =  0
    """int: how many arguments were given """

    newlist     = []
    """list: changed filenames """

    oldlist     = []
    """list: unchanged filenames """

    rename_list = []
    """list: list of files to rename """

    capitalize  = False
    lowercase   = False
    uppercase   = False
    Titlecase   = False
    no_root_warning = False

    action      = None

    if len(sys.argv) < 2:
        usage();
        exit(2)

    thisfile = os.path.basename(sys.argv[0]) # skip this file
    # parse options and return arglength args
    numargs, args, flags =  parse_args(sys.argv[1:] ) 

  
    debug( "flags:\t" + str(flags) )

#    "options": {
#        "short": "hiultTv" ,
#        "long": [ "help" , "interactive", "upper", "lower", "test", "Title", "verbose" ]

    # parse option flags
    for k,v  in flags:

        if k in ( "help" ):
            usage()
            sys.exit(0)

        elif k in ( "interactive" ):
            interactive = True
            force       = False

        elif k in ( "force" ):
            if not interactive:
              force = True

        elif k in ( "lower" ):
            lowercase = True
            uppercase = False

        elif k in ( "recursive" ):
            recursive = True

        elif k in ( "override_root_warning" ):
            if os.geteuid() == 0:
                no_root_warning = True

        elif k in ( "test" ):
            test = True

        elif k in ( "Title" ):
            Titlecase = True
            uppercase = False

        elif k in ( "upper" ):
            uppercase = True            

        elif k in ( "verbose" ):
            verbose = True
        else:
            capitalize = True

    if os.geteuid() == 0:  # remind superuser of danger
        if not no_root_warning:
            eprint("WARNING -- super user invocation. Use Caution.")


    if (lowercase and uppercase) :
        eprint( "OPTIONS ERROR: can't have lower and upper together.")
        usage()
        sys.exit(2)

    if (Titlecase and (lowercase or uppercase)):
        eprint( "OPTIONS ERROR can't have Titlecase and lower or upper together.")
        usage()
        sys.exit(2)

    if uppercase:
        action = "upper"
    elif lowercase:
        action = "lower"
    elif Titlecase:
        action = "title"
    else:
        action = "capitalize"


    debug( "thisfile:\t" + thisfile ) 


    if thisfile in args:
        args.remove(thisfile)

    for filename in args:

      if not os.path.exists(filename):
        args.remove(filename)

        continue 

      rename(action, filename)


#        arg = os.path.abspath(fn)

#END
