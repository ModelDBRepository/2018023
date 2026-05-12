"""turn off AP stim when AP occurs so there is no artifact as there
is when the iclamp turns off later
See setup_tGARs.py for where myadvance() takes care of turning off the iclamp
and then resetting it to iclamp amp's orig value when sim over.

"""

from setup_tGARs import *

h(""" 
objref p
p = new PythonObject()
proc my_run() {
p.my_run($1)
}
proc advance() {
p.myadvance()
}
""")
