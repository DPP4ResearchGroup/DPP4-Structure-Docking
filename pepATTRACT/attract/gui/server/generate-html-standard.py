import sys, os
sys.path.insert(0, "..")
import spyder
spyder.silent = True
from attractmodel import AttractEasyModel
import form_standard

cgi = sys.argv[1]

f = AttractEasyModel._form()
f = form_standard.webform(f)
html = form_standard.html(f, cgi, None, newtab=True)
print(html)