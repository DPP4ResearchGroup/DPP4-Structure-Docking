header = """<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    
    <head>
        <title>ATTRACT Peptide Online</title>
        
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
                <li id="view-page2"><a id="nav-block-energy" class="energy-icon">Energy and Interaction</a></li>
                <li id="view-page3"><a id="nav-block-analysis" class="analysis-icon">Analysis</a></li>
                <li id="view-page4"><a id="nav-block-computation" class="computation-icon">Computation</a></li>
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

def webform(f, model=None):
  import copy
  f = copy.deepcopy(f)  
  f.resourcefilevar = "_tempresource"
  f.arraymarker = "_clonearraymarker"


  f.completion_tool.type = None #hide in web interface
  
  ### START partners category
  c = f.new_group("c_partners", "category")
  c.page = 1
  c.icon = "puzzle-icon"
  c.title = "Docking partners"
  c.categoryname = "partners"
  c.description = """Define protein and peptide by uploading a PDB structure file and a sequence.""" 
  
  bp1 = f.new_group("bp1","block")
  c.members.append("bp1")
  bp1.title = "Protein"
  bp2 = f.new_group("bp2","block")
  c.members.append("bp2")
  bp2.title = "Peptide"
  
  
  bp1.members.append("p1")   
  f.p1.controltitle = ""
  f.p1.name = ""
  f.p1.has_hydrogens.type = None #hide in web interface
  
  fp = f.p1
  fp.group = None  
  b = fp.new_group("b_struc","block")
  b.title = "Structure Sources"
  b.has_switch = False
  b.members.append("pdbfile")
  ff = fp.pdbfile
  ff.name = "Structure file"
  ff.tooltip = "Upload PDB structure file"
  ff.tooltip_doc = "documentation.html#partners-structure_file"
  ff.span = True
  b.members.append("ensemble_size")
  ff = fp.ensemble_size
  ff.tooltip_doc = "documentation.html#partners-ensemble_size"
  ff.span = True
  fp.haddock_restraints.span = True
  ### END b_struc block


  ### START b_rmsd block
  b = fp.new_group("b_rmsd", "block")
  b.title = "RMSD calculation"
  b.members.append("use_rmsd")
  b.has_switch = True
  b.members.append("rmsd_pdb")
  ff = fp.use_rmsd
  ff.default = False
  ff.type = "switch" 
  ff.name = "RMSD calculation"
  ff = fp.rmsd_pdb
  ff.name = "Reference RMSD PDB file"
  ### END b_rmsd block

  

  bp2.members.append("p2")
  f.p2.controltitle = ""
  f.p2.name = ""
  fp = f.p2
  fp.group = None
  fp.multi_active = True
  b = fp.new_group("b_struc","block")
  b.title = "Structure Sources"
  b.has_switch = False
  b.members.append("sequence")
  ff = fp.sequence  
  ff.tooltip = "Give peptide sequence in single letter code"
  ff.span = True
  ### END b_struc block

  ### START b_rmsd block
  b = fp.new_group("b_rmsd", "block")
  b.title = "RMSD calculation"
  b.members.append("use_rmsd")
  b.has_switch = True
  b.members.append("rmsd_pdb")
  ff = fp.use_rmsd
  ff.default = False
  ff.type = "switch" 
  ff.name = "RMSD calculation"
  ff = fp.rmsd_pdb
  ff.name = "Reference RMSD PDB file"
  ### END b_rmsd block

 

  ### START energy category
  c = f.new_group("c_energy", "category")
  c.page = 2
  c.icon = "energy-icon"
  c.title = "Energy and Interaction"
  c.always_active = True
  c.categoryname = "energy"
  c.description = ""
  _assign_category(f, c, "Energy and interaction parameters", span = True)
  ### END energy category  

  ### START analysis category
  c = f.new_group("c_analysis", "category")
  c.page = 3
  c.icon = "analysis-icon"
  c.title = "Analysis"
  c.always_active = True
  c.categoryname = "analysis"
  c.description = ""
  _assign_category(f, c, "Analysis")
  ff = f.nr_collect
  ff.span = True  
  ### END analysis category

  ### START computation category
  c = f.new_group("c_computation", "category")
  c.page = 4
  c.icon = "computation-icon"
  c.title = "Computation"
  c.always_active = True
  c.categoryname = "computation"
  c.description = ""
  _assign_category(f, c, "Computing and parallelization parameters", span = True)
  c.members.insert(0, "runname")
  ### END computation block

  return f

def webserverform(webdict, form=None, spydertype=None):
  if spydertype is not None: form = spydertype._form()
  f = webform(form)
  return f
  
def html(form, cgi, spyderobj, newtab=False):
  from form_model import html
  return html(form, cgi, spyderobj, newtab, header=header)
