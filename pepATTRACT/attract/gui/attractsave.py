import os
import Spyder

from spyder.formtools import make_relpath, check_embedded
  
def save(m, outp, *args):
  v = m._get()   
  outpdir = os.path.split(outp)[0]  
  if v is not None:
    make_relpath(outpdir, v)
    v.tofile(outp)
    print("Form object saved to %s" % outp)
  else:
    print("Cannot save form: does not contain a valid object")

def generate(m, outp, *args):
  v = m._get() 
  outpdir = os.path.split(outp)[0]
  if v is not None: 
    if isinstance(v, Spyder.AttractPeptideModel):
      v = v.convert(Spyder.AttractEasyModel) 
      r = v.partners[1].pdbfile
      r.link("./peptide.pdb")
      r.save()
    
    embedded = check_embedded(v)
    if embedded is not None:
      print("Cannot generate shell script: %s is an embedded resource, not a file name" % embedded)
      return
    make_relpath(outpdir, v)
    sh = os.path.splitext(outp)[0] + ".sh"
    script = v.generate()
    fsh = open(sh, "w")
    fsh.write(script+"\n")
    fsh.close()
    os.system("chmod +x %s" % sh)
    print("Shell script generated: %s" % sh)
  else:
    print("Cannot generate shell script: form does not contain a valid object")
    
def _deploy(resource, fname):
  if resource is not None: 
    resource.link(fname)
    resource.save()
  
def deploy(model, dir):
  d = dir + "/"
  if dir in (None, "", ".", "./"): d = ""
  elif dir.endswith("/"): d = dir
  for n,p in enumerate(model.partners):
    _deploy(p.pdbfile,d+"partner-%d.pdb" % (n+1))
    _deploy(p.rmsd_pdb,d+"partner-rmsd-%d.pdb" % (n+1))
    _deploy(p.rmsd_pdb_alt,d+"partner-rmsd-alt-%d.pdb" % (n+1))
    _deploy(p.rmsd_pdb_alt2,d+"partner-rmsd-alt2-%d.pdb" % (n+1))
  _deploy(model.start_structures_file,d+"startstruc.dat")
  _deploy(model.rotations_file,d+"rotations.dat")
  _deploy(model.translations_file,d+"translations.dat")
  _deploy(model.harmonic_restraints_file,d+"harmonic-restraints.tbl")
  _deploy(model.haddock_restraints_file,d+"haddock-restraints.tbl")
  _deploy(model.position_restraints_file,d+"position-restraints.tbl")

def deploy_easy(model, dir):
  d = dir + "/"
  if dir in (None, "", ".", "./"): d = ""
  elif dir.endswith("/"): d = dir
  _deploy(model.partners[0].pdbfile,d+"receptor.pdb")
  _deploy(model.partners[0].rmsd_pdb,d+"receptor-rmsd.pdb")
  _deploy(model.partners[1].pdbfile,d+"ligand.pdb")
  _deploy(model.partners[1].rmsd_pdb,d+"ligand-rmsd.pdb")
  _deploy(model.harmonic_restraints_file,d+"harmonic-restraints.tbl")
  _deploy(model.position_restraints_file,d+"position-restraints.tbl")

def deploy_narefine(model, dir):
  d = dir + "/"
  if dir in (None, "", ".", "./"): d = ""
  elif dir.endswith("/"): d = dir
  _deploy(model.pdbfile,d+"input.pdb")
   
def deploy_peptide(model,dir):
  d = dir + "/"
  if dir in (None, "",".","./"): d = ""
  elif dir.endswith("/"): d = dir
  _deploy(model.p1.pdbfile,d+"receptor.pdb")
  _deploy(model.p1.rmsd_pdb,d+"receptor-rmsd.pdb")
  _deploy(model.p2.rmsd_pdb,d+"peptide-rmsd.pdb")
