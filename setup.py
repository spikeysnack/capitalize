import sys, os, errno
import  shutil
from distutils.core import setup

files = ["*"]

setup(name='capitalize',
      version='1.2',
      description='change case in a list of filenames',
      url='https://sites.google.com/site/drudgeryville/',
      author='Chris Reid',
      author_email='spikeysnack@gmail.com',
      license='Creative Commons Non-commercial 4.0',
      long_description = r""" A tool to change the capitalization 
                            in a list of file names. """,
      platforms=['Linux', 'BSD', 'MACOSX', 'MSWindows', 'noarch'],
      keywords='batch renaming',
      classifiers=[ 'Development Status :: 4 - Beta', 
                   'Intended Audience :: Users',
                   'Topic :: File Utilities :: Batch Renamers',
                   'License :: Creative Commons :: Non-Commercial4.0 License',
                   'Programming Language :: Python',
                 ],
      provides=['capitalize'],
      packages=['capitalize'],
      requires=['getopts','string'],
      data_files=[ ('doc/capitalize', [ 'doc/css/base.css', 'doc/css/button.png', 
                                     'doc/css/light.css',  'doc/capitalize.html',  'doc/capitalize.png']),
                  ('man/man1' , ['doc/capitalize.1']),
                  ('doc/capitalize' , ['doc/README'])], 
      scripts=['capitalize.py'])



def force_symlink(file1, file2):
    try:
        os.symlink(file1, file2)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)


#print ( "args:\t" + str(sys.argv) )


# force install of man page
if 'install' in sys.argv:

    if '--user' in sys.argv:
        homedir = os.path.expanduser('~')
        man_path = homedir + "/.local/man/man1/"
    else:
        man_path = "/usr/local/share/man/man1/"
 
    if os.path.exists(man_path): 
        print("Installing man pages") 
        man_page = "capitalize.1" 
        shutil.copy2('doc/'+ man_page, man_path) 
        os.chmod(man_path + 'capitalize.1', int('444', 8)) 

    src = "capitalize.py"

    if '--user' in sys.argv:
        homedir = os.path.expanduser('~')
        path= homedir + "/bin/"
    else:
        path = "/usr/local/bin/"

        
    if os.path.exists(src):
        force_symlink( path + src, path + "capitalize" )
