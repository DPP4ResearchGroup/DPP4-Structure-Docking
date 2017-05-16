import sys, os
sys.path.insert(0, "..")
import spyder
spyder.silent = True
from attractmodel import AttractModel
import form_model

cgi = sys.argv[1]

f = AttractModel._form()
f = form_model.webform(f)
html = form_model.html(f, cgi, None, newtab=True)
print(html)