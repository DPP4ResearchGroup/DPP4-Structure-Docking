header = """<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    
    <head>
        <title>ATTRACT Online</title>
        
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <meta name="description" content="" />
        <meta name="viewport" content="width=device-width"/>
        
        <!-- Always load normalize CSS first -->
        <link rel="stylesheet" href="css/normalize.min.css">
        <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,600' rel='stylesheet' type='text/css'>
        <link href='http://fonts.googleapis.com/css?family=Lobster' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="css/attract.min.css">
    </head>
    
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <main id="container" class="col row">
          
          <section id="sidebar" class="col">
            <div id="title"><span class="t1">Attract</span> <span class="t2">online</span></div>
            <div id="logo"></div>
            
            <nav id="form-category-navigation" class="row">
              <ul>
                <li id="view-page1"><a id="nav-block-partners" class="puzzle-icon">Partners</a></li>
                <li id="view-page2"><a id="nav-block-grids" class="grid-icon">Grids</a></li>
                <li id="view-page3"><a id="nav-block-iterations" class="iteration-icon">Iteration</a></li>
                <li id="view-page4"><a id="nav-block-sampling" class="sampling-icon">Sampling</a></li>
                <li id="view-page5"><a id="nav-block-energy" class="energy-icon">Energy and Interaction</a></li>
                <li id="view-page6"><a id="nav-block-atomdensitygrid" class="cryo-icon">Atom density grids</a></li>
                <li id="view-page7"><a id="nav-block-symmetry" class="symmetry-icon">Symmetry</a></li>
                <li id="view-page8"><a id="nav-block-analysis" class="analysis-icon">Analysis</a></li>
                <li id="view-page9"><a id="nav-block-computation" class="computation-icon">Computation</a></li>
              </ul>
            </nav>
            
            <div id="download-button" class="row download-icon" onClick="submitForm();">
              <p>Get configuration</p>
            </div>  
            
          </section>
            
          <section id="content" class="col">
            
            <header id="header">
              
              <div id="show-hide-sidepanel" class="button menu-icon float-left"><div class="header-tooltip"><p>Hide sidepanel</p></div></div>
              <div id="reload-form" class="button reload-icon-active float-left"><div class="header-tooltip"><p>Restore default values</p></div></div>
              <div id="unfold-all" class="button double-arrow-icon float-left"><div class="header-tooltip"><p>Unfold all form blocks</p></div></div>
              <div id="header-nav" class="button-text down-icon-active float-left">
                <p>Menu</p>
                <nav class="header-tooltip">
                  <ul>
                    <li><a href="#" class="download-icon" onClick="submitForm();">Save</a></li>
                    <li><a href="documentation.html#contact" target="_blank" class="contact-icon">Contact</a></li>
                    <li><a href="documentation.html" target="_blank" class="help-icon">Help and documentation</a></li>
                  </ul>
                </nav> 
              </div>
              <div id="close-app" class="button close-icon-active float-right"></div>
              
            </header>
"""

footer = """           
            
        </section>
      </main>  
        
      <script src="js/jquery-1.10.2.min.js"></script>
      <script src="js/main.min.js"></script>

    </body>
</html>"""

def _assign_category(f, category, groupname, span = False):
  for member in f._membernames:
    ff = getattr(f, member)
    if not hasattr(ff, "group"): continue
    if ff.group != groupname: continue
    category.members.append(member)
    ff.group = None
    if span: ff.span = True

def webform(f, model=None,
 partnerslength=None, gridslength=None, iterationslength=None, symmetrieslength=None,
):
  if model is not None:
    if partnerslength is None:
      partnerslength = max(1,len(model.partners))
    if gridslength is None:
      gridslength = max(1,len(model.grids))
    if iterationslength is None:
      iterationslength = max(1,len(model.iterations))
    if symmetrieslength is None:  
      symmetrieslength = max(1,len(model.symmetries))
  else:  
    if partnerslength is None: partnerslength = 1
    if gridslength is None: gridslength = 1  
    if iterationslength is None: iterationslength = 1
    if symmetrieslength is None: symmetrieslength = 1
  import copy
  f = copy.deepcopy(f)
  f.arraymarker = "_clonearraymarker"
  f.resourcefilevar = "_tempresource"
  
  f.partners.length = partnerslength
  
  ### START partners category
  c = f.new_group("c_partners", "category")
  c.page = 1
  c.icon = "puzzle-icon"
  c.title = "Docking partners"
  c.categoryname = "partners"
  c.description = """Define up to 10 docking partners by uploading a PDB structure file or identifying them by their 
            RCSB Protein Databank ID. Ensemble structures are allowed.""" 
  c.members.append("partners")   
  f.partners.clonebutton = "Add partner"
  f.partners.clonelength = 10
  f.partners.controltitle = "Docking partners"  
  for fpnr in range(f.partners.length):
    fp = f.partners[fpnr]
    fp.group = None
    
    ### START b_struc block
    b = fp.new_group("b_struc", "block")
    b.title = "Structure Sources"
    b.has_switch = False
    b.members.append("pdbfile")
    b.members.append("gridname")
    b.members.append("chain")    
    b.members.append("moleculetype") 
    ff = fp.pdbfile
    ff.name = "Structure file"
    ff.tooltip = "Upload PDB structure file"
    ff.tooltip_doc = "documentation.html#partners-structure_file"
    ff = fp.gridname
    ff.name = "Name of the grid for this molecule"
    ff.tooltip = "Grid name"
    ff.tooltip_doc = "documentation.html#partners-grid_name"
    ff = fp.chain
    ff.name = "Which chain must be used?"
    ff.default = "All"
    ff.tooltip = "Which chain ID"
    ff.tooltip_doc = "documentation.html#partners-chains"
    ### END b_struc block

    ### START b_modes block
    b = fp.new_group("b_modes", "block")
    b.title = "Use harmonic modes"
    #insert placeholder boolean to determine the state of the Modes switch
    if "use_modes" not in fp._membernames:
      fp._membernames.append("use_modes")
    fp._members["use_modes"] = fp._members["ensemble"].get_copy()        
    b.members.append("use_modes")
    b.has_switch = True
    b.members.append("generate_modes")
    b.members.append("aacontact_modes")
    b.members.append("nr_modes")
    ff = fp.use_modes
    ff.name = "Use harmonic modes"
    ff.type = "switch"    
    ff = fp.generate_modes
    ff.name = "Or: generate harmonic modes automatically"
    ff = fp.nr_modes
    ff.name = "Number of modes to select"
    ff.type = "number"
    ff.min = 1
    ff.max = 10
    ### END b_modes block

    ### START b_ensemble block
    b = fp.new_group("b_ensemble", "block")
    b.title = "Use ensembles"
    b.members.append("ensemble")
    b.has_switch = True
    b.members.append("ensemble_size")
    b.members.append("ensemblize")
    ff = fp.ensemble
    ff.type = "switch"
    ff.name = "Use ensembles"
    ff = fp.ensemble_size
    ff.min = 1
    ff = fp.ensemblize
    ### END b_ensemble block

    ### START b_rmsd block
    b = fp.new_group("b_rmsd", "block")
    b.title = "RMSD calculation"
    #insert placeholder boolean to determine the state of the RMSD switch
    if "rmsd" not in fp._membernames:
      fp._membernames.append("rmsd")
    fp._members["rmsd"] = fp._members["ensemble"].get_copy()
    b.members.append("rmsd")
    b.has_switch = True
    b.members.append("rmsd_pdb")
    b.members.append("rmsd_pdb_alt")
    b.members.append("rmsd_pdb_alt2")
    ff = fp.rmsd
    ff.default = True
    ff.name = "RMSD calculation"
    ff = fp.rmsd_pdb
    ff.name = "Reference RMSD PDB file"
    ff.span = True
    ### END b_rmsd block
  ### END partners category

  ### START grids category
  c = f.new_group("c_grids", "category")
  c.page = 2
  c.title = "Grids"
  c.icon = "grid-icon"
  c.categoryname = "grids"
  c.description = ""
  c.members.append("grids")
  f.grids.length = gridslength
  f.grids.clonebutton = "Add grid"
  f.grids.clonelength = 10
  f.grids.controltitle = "Grid"
  f.grids.group = None
  fg = f.grids[0]

  b = fg.new_group("b_grids", "block")
  b.title = None
  b.members.append("gridname")  
  b.members.append("plateau_distance")
  b.members.append("neighbour_distance")
  b.members.append("omp")
  b.members.append("torque")
  b.members.append("calc_potentials")
  ff = fg.gridname
  ff.placeholder = "name..."
  for n in range(f.grids.length):
    ff = f.grids[n]      
  ff = fg.omp
  ff.name = "Calculate grid using OpenMP?"
  ff = fg.torque  
  ff = fg.plateau_distance
  ff = fg.neighbour_distance
  ### END grids category

  ### START iteration category
  c = f.new_group("c_iterations", "category")
  c.page = 3
  c.title = "Iteration"
  c.icon = "iteration-icon"
  c.categoryname = "iterations"
  c.description = ""
  c.members.append("iterations")
  f.nr_iterations.type = None #hide explicit nr_iterations parameter
  f.nr_iterations.group = None
  f.iterations.group = None
  f.iterations.length = iterationslength
  f.iterations.clonebutton = "Add iteration"
  f.iterations.clonelength = 5
  f.iterations.controltitle = "Iteration"

  for fi in [f.iterations[i] for i in range(f.iterations.length)]:
    fi.name = None
    fi.group = None
    ff = fi.rcut
    ff.span = True
    ff = fi.vmax
    ff.span = True
    ff = fi.traj
    ff.span = True 
    fi.memberorder = ["rcut", "vmax", "traj", "mc"]
    b = fi.new_group("b_mc", "block")
    b.insert_at_member = True
    b.has_switch = True
    _assign_category(fi, b, "Monte Carlo", span = True)
    b.members.remove("mc")
    b.members.insert(0, "mc")
    ff = fi.mc
    ff.type = "switch"
  ### END iteration category  

  ### START sampling category
  c = f.new_group("c_sampling", "category")
  c.page = 4
  c.icon = "sampling-icon"
  c.title = "Sampling"
  c.categoryname = "sampling"
  c.description = ""
  f.iattract.group = None
  _assign_category(f, c, "Sampling parameters", span = True)
  f.start_structures_file.title = "Custom search files"
  f.use_iattract.add_header("iATTRACT parameters")
  c.members.append("iattract.nstruc")
  c.members.append("iattract.icut")
  ### END sampling category  

  ### START energy category
  c = f.new_group("c_energy", "category")
  c.page = 5
  c.icon = "energy-icon"
  c.title = "Energy and Interaction"
  c.categoryname = "energy"
  c.description = ""
  f.atomdensitygrids.group = None
  _assign_category(f, c, "Energy and interaction parameters", span = True)
  f.gravity.default = 0
  f.ghost.name = "Enable ghost mode, forcefield is turned off"
  ### END energy category  
  
  ### START atomdensitygrid category
  c = f.new_group("c_atomdensitygrid", "category")
  c.page = 6
  c.title = "Atom density grids"
  c.icon = "cryo-icon"  
  c.categoryname = "atomdensitygrids"
  c.description = ""  
  c.members.append("atomdensitygrids")
  ff = f.atomdensitygrids  
  ff.clonebutton = "Add atom density grid"
  ff.length = 1
  ff.clonelength = 3
  ff.blockname = "atomdensitygrid"
  ff.controltitle = "Atom density grid"  

  ### START symmetry category
  c = f.new_group("c_symmetry", "category")
  c.page = 7
  c.title = "Symmetry"
  c.icon = "symmetry-icon"
  c.categoryname = "symmetry"
  c.description = """      <p>You can use generative symmetry or distance-restrained symmetry. If you want to use generative symmetry:</p>
        <ul>
          <li>Provide an explicit symmetry axis and origin</li>
          <li>Specify a single reference symmetry partner</li>
          <li>In the Docking Partner section, only define the reference partner structure</li>
        </ul>
        If you want to use distance-restrained symmetry:
        <ul>
          <li>Do not provide explicit symmetry axis and origin</li>
          <li>Specify all symmetry partners that are to be restrained</li>
          <li>In the Docking Partner section, specify all partner structures, which must be identical</li>
        </ul>"""
  c.html_description = True      
  c.members.append("symmetries")
  f.symmetries.length = symmetrieslength #TODO
  f.symmetries.clonebutton = "Add partner"
  f.symmetries.clonelength = 5
  f.symmetries.blockname = "symmetry"
  f.symmetries.controltitle = "Symmetry"

  fs = f.symmetries[0]
  fs.symmetry_axis.x.name = "X"
  fs.symmetry_origin.x.name = "X"
  fs.symmetry_axis.y.name = "Y"
  fs.symmetry_origin.y.name = "Y"
  fs.symmetry_axis.z.name = "Z"
  fs.symmetry_origin.z.name = "Z"
  b = fs.new_group("b_symmetry", "block")
  b.title = "Generative symmetry axis"
  b.title2 = "Origin for generative symmetry axis"
  b.members.append("symmetry_axis.x")
  b.members.append("symmetry_origin.x")
  b.members.append("symmetry_axis.y")
  b.members.append("symmetry_origin.y")
  b.members.append("symmetry_axis.z")
  b.members.append("symmetry_origin.z")
  b.members.append("symmetry")
  ### END symmetry category  

  ### START analysis category
  c = f.new_group("c_analysis", "category")
  c.page = 8
  c.icon = "analysis-icon"
  c.title = "Analysis"
  c.categoryname = "analysis"
  c.description = ""
  _assign_category(f, c, "Analysis")
  c.members.remove("rcut_rescoring")
  c.members.insert(c.members.index("nr_collect"), "rcut_rescoring")
  ff = f.rcut_rescoring
  ff.span = True
  ff = f.nr_collect
  ff.span = True  
  ff = f.deflex
  ff.tooltip = "Remove flexibility"
  ff.tooltip_doc = "documentation.html#partners-no_flex"  
  ### END analysis category

  ### START computation category
  c = f.new_group("c_computation", "category")
  c.page = 9
  c.icon = "computation-icon"
  c.title = "Computation"
  c.categoryname = "computation"
  c.description = ""
  f.header.rows = 25
  _assign_category(f, c, "Computing and parallelization parameters", span = True)
  c.members.insert(0, "runname")
  ### END computation category

  return f

import os

def webserverform(webdict, form=None, spydertype=None):
  if spydertype is not None: form = spydertype._form()
  f = webform(
   form,
   partnerslength = 10,
   gridslength = 10,
   symmetrieslength = 10,
   iterationslength = 10,
  )  
  nr_iterations = 0
  try:
    nr_iterations = len(webdict["iterations"])
  except (KeyError, TypeError) as exc:
    pass
  webdict["nr_iterations"] = nr_iterations
  return f

header0 = header
footer0 = footer  
def html(form, cgi, spyderobj, newtab=False, header=header0, footer=footer0):
  import random
  import attracthtmlform 
  args = dict (
   obj=spyderobj,
   form=form, cgi=cgi, 
   header=header, footer=footer, header_indentation = 12, 
   newtab=newtab,
  )
  if spyderobj is not None:
    from spyder.formtools import embed
    embed(spyderobj)
    mydir = "attractrun" + str(random.randint(1,1000000))  
    fname = "attract.web"
    os.chdir("/tmp/")
    os.mkdir(mydir)
    os.chdir(mydir)
    spyderobj.tofile(fname)
    args["resourcefilename"] = mydir+"/"+fname
  html = attracthtmlform.htmlform(**args)
  return html
  