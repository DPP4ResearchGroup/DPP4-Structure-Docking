//Scores mode deformations using an explicit elastic network

//usage: ./score-deform structures.dat ligands.pdb [--modes <modefile>] [--ens/--morph <ligand nr> <ensemble file>]

#include "max.h"
#include <cmath>
#include <cstdio>

extern int cartstate_new(int argc, char *argv[],bool single=0);

extern "C" void cartstate_set_pivot_(const int &handle, double (&pivot)[3][MAXLIG]);
extern "C" void cartstate_pivot_auto_(const int &handle);

extern "C" void cartstate_f_write_pdb_(
  const int &handle,
  int &nlig, int *&kai, char4 *&tyi, char4 *&rgi, int *&iei, double *&x,
  int *&iaci, double *&xlai, int *&icop, double *&we, int *&ieins);

extern "C" void cartstate_f_rotdeform_(
  const int &handle,
  int *(&nhm), int *&ieins, double *&eig, double *&pivot, double *&xb, double *&x,double *&xori, double *&xori0);

extern "C" void cartstate_get_nlig_nhm_(const int &handle, int &nlig, int *(&nlm));
extern "C" void cartstate_get_pivot_(const int &handle,double *&pivot);
extern "C" void cartstate_get_nrens_(const int &handle,int *&nrens);

extern "C" void cartstate_get_ensd_(const int &handle,
  const int &ligand,
  const int &ens,
  double *&ensd,
  const double &morph,
  double &cmorph,
  double *&cmorphd
  );
  
extern "C" FILE *read_dof_init_(const char *f_, int nlig, int &line, double (&pivot)[3][MAXLIG], int &auto_pivot, int &centered_receptor, int &centered_ligands, int f_len);

extern "C" int read_dof_(FILE *fil, int &line, int &nstruc, const char *f_, idof2 &ens, dof2 &phi, dof2 &ssi, dof2 &rot, dof2 &xa, dof2 &ya, dof2 &za, coors2 &locrests, dof2 &morph, modes2 &dlig, const int &nlig, const int *nhm, const int *nrens0, const int *morphing, const int *has_locrests, int &seed, char *&label, const int &all_labels, int f_len);

extern "C" void deformscore_(
  const int &totmaxatom, const int &maxlig, const int &nlig,
  int *kai, char4 *tyi, char4 *rgi, int *iei, double *x,
  int *iaci, double *xlai, int *icop, double *we, int *ieins, double *score);

extern "C" void euler2rotmat_(const double &phi,const double &ssi, const double &rot, double (&rotmat)[9]);

extern "C" void rotate_(const int &maxlig,const int &max3atom,double (&rotmat)[9],const double &xa,const double &ya,const double &za,
double *pivot,
int &ijk,int *ieins, double *x);

extern "C" void deform_(const int &maxlig,const int &max3atom, 
const int &totmax3atom, const int &maxatom,const int &maxmode,
int &ens, double *ensdp, const double &cmorph, const double *cmorphdp, 
double (&dligp)[MAXMODE], 
int *nhm,int &ijk,int *ieins,double *eig,double *xb,double *x,double *xori,double *xori0, const int &do_morph); 

/*support for non-reduced PDBs*/
#include "state.h"

extern void read_ens(int cartstatehandle, int ligand, char *ensfile, bool strict, bool morphing);

CartState &cartstate_get(int handle);

/* DOFs */
static int ens[MAXLIG];
static double morph[MAXLIG];
static double phi[MAXLIG];
static double ssi[MAXLIG];
static double rot[MAXLIG];
static double xa[MAXLIG];
static double ya[MAXLIG];
static double za[MAXLIG];
static double dlig[MAXLIG][MAXMODE];
static int seed;
static char *label;

#include <cstdio>
#include <cstring>
#include <cstdlib>

void usage() {
  fprintf(stderr, "usage: score-deform structures.dat ligands.pdb [--modes <modefile>] [--ens/--morph <ligand nr> <ensemble file>\n");
  exit(1);
}

extern bool exists(const char *f);

int main(int argc, char *argv[]) {
  int i;
  if (argc < 3) {
    fprintf(stderr, "Too few arguments\n"); usage();
  }
  for (i = 1; i <= 2; i++) {
    if (!exists(argv[i])) {
      fprintf(stderr, "File %s does not exist\n", argv[i]);
      exit(1);
    }
  }

  coors2 locrests;
  int has_locrests[MAXLIG];
  memset(has_locrests, 0, MAXLIG*sizeof(int));
  
  char *modefile = NULL;
  int enscount = 0;
  int ens_ligands[MAXLIG];
  char *ens_files[MAXLIG];
  int morphing[MAXLIG];
  memset(morphing,0,MAXLIG*sizeof(int));
  for (int n = 1; n < argc-1; n++) {
    if (!strcmp(argv[n],"--modes")) {
      modefile = argv[n+1];
      char **argv2 = new char *[argc-1];
      if (n > 0) memcpy(argv2, argv,n*sizeof(char*));
      if (n+2 < argc) memcpy(argv2+n,argv+n+2,(argc-n-2)*sizeof(char*));
      argv = argv2;
      argc -= 2;
      break;
    }
  }
  for (int n = 1; n < argc-2; n++) {
    bool has_ens = 0;        
    if (!strcmp(argv[n],"--ens")) {
      has_ens = 1;
    }
    if (!strcmp(argv[n],"--morph")) {
      morphing[enscount] = 1;
      has_ens = 1;
    }    
    if (has_ens) {
      ens_ligands[enscount] = atoi(argv[n+1]);
      ens_files[enscount] = argv[n+2];
      enscount++;
      char **argv2 = new char *[argc-1];
      if (n > 0) memcpy(argv2, argv,n*sizeof(char*));
      if (n+3 < argc) memcpy(argv2+n,argv+n+3,(argc-n-3)*sizeof(char*));
      argv = argv2;
      argc -= 3;
      n -= 1;
    }    
  }  
  for (int n = 1; n < argc-1; n++) {
    if (!strcmp(argv[n],"--locrest")) {
      int lig = atoi(argv[n+1]);
      if (lig <= 0 || lig > MAXLIG) {
        fprintf(stderr,"Ligand %d must be larger than 0\n", lig);
        usage();
      }
      has_locrests[lig-1] = 1;
      char **argv2 = new char *[argc-1];
      if (n > 0) memcpy(argv2, argv,n*sizeof(char*));
      if (n+2 < argc) memcpy(argv2+n,argv+n+2,(argc-n-2)*sizeof(char*));
      argv = argv2;
      argc -= 2;
      n -= 1;
    }
  }

  //load the Cartesian parameters and get a handle to it
  int cartstatehandle;
  if (argc == 3) { //one PDB, reduced or non-reduced
    char *argv0[] = {NULL, argv[2]};
    cartstatehandle = cartstate_new(2, argv0);
  }
  else {
    fprintf(stderr, "Wrong number of arguments\n"); usage();    
  }

  CartState &cs = cartstate_get(cartstatehandle);  
  memcpy(cs.xori,cs.xori0,TOTMAXATOM*3*sizeof(double));  
  if (modefile != NULL) {
    const int multi = 1;
    read_hm_(modefile,"ligand",cs.nlig, cs.natom, cs.nhm, cs.val, (double *) cs.eig, multi, strlen(modefile), strlen("ligand"));
  }
      
  for (int n = 0; n < enscount; n++) {
    read_ens(cartstatehandle, ens_ligands[n]-1, ens_files[n], 0, morphing[n]);
  }      
      
  //retrieve the parameters needed to read the DOFs
  int nlig; int *nhm;
  cartstate_get_nlig_nhm_(cartstatehandle, nlig,nhm);
  
  int nrdof = 6 * nlig;
  for (int n = 0; n < nlig; n++) nrdof += nhm[n];
  if (nrdof > MAXDOF) {
    fprintf(stderr, "Too many DOFs: %d, MAXDOF=%d\n",nrdof, MAXDOF); 
    exit(1);
  }
  
  //read DOFs and set pivots
  //fpivot contains any pivots read from the DOF file
  double fpivot[3][MAXLIG];
  int auto_pivot, centered_receptor, centered_ligands;  
  int line;
  FILE *fil = read_dof_init_(argv[1], nlig, line, fpivot, auto_pivot, centered_receptor, centered_ligands, strlen(argv[1]));
  if (auto_pivot) cartstate_pivot_auto_(cartstatehandle);
  else cartstate_set_pivot_(cartstatehandle, fpivot);  
  
  double *pivot; //the actual pivots (from file or auto-calculated)
  
  int *kai;char4 *tyi;char4 *rgi; int *iei; 
  double *x; int *iaci; double *xlai; int *icop; double *we; int *ieins;
  double *eig; double *xb; double *dmmy1; double *dmmy2;
    
  //get the Cartesian parameters we need for rotation and deformation
  cartstate_f_rotdeform_(cartstatehandle,
   nhm, ieins, eig, pivot, xb, x, dmmy1, dmmy2);
  int *nrens; //the ensemble size for each ligand
  cartstate_get_nrens_(cartstatehandle,nrens);
    
  //get the Cartesian parameters we need for score calculation
  // (same as for PDB writeout)
  cartstate_f_write_pdb_(cartstatehandle,
   nlig, kai,tyi,rgi,iei,x,iaci,xlai,icop,we,ieins); 
  
  //main loop
  int nstruc = 0;  
  while (1) {
    
    int result = read_dof_(fil, line, nstruc, argv[1], ens, phi, ssi, rot, 
     xa, ya, za, locrests, 
     morph, dlig, nlig, nhm, nrens, morphing, has_locrests,
     seed, label, 0, strlen(argv[1])
    );
    if (result != 0) break;

    if (centered_receptor) { //...then subtract pivot from receptor
      xa[0] -= pivot[0];
      ya[0] -= pivot[MAXLIG];
      za[0] -= pivot[2*MAXLIG];
    }
    

    if (centered_ligands) { //...then subtract pivot from all (other) ligands 
      for (i = 1; i < nlig; i++) {
        xa[i] -= pivot[i];
	ya[i] -= pivot[MAXLIG+i];
	za[i] -= pivot[2*MAXLIG+i];
      }
    }          
    for (i = 0; i < nlig; i++) {

      //Get ensemble differences
      double *ensdp;
      double cmorph;
      double *cmorphdp;
      cartstate_get_ensd_(cartstatehandle, i, ens[i], ensdp,
      morph[i],cmorph, cmorphdp);

      //Apply harmonic modes
      double (&dligp)[MAXMODE] = dlig[i];
      deform_(MAXLIG, 3*MAXATOM, 3*TOTMAXATOM, MAXATOM,MAXMODE, 
        ens[i], ensdp, cmorph, cmorphdp, dligp, nhm, i, ieins, eig, xb, x, dmmy1, dmmy2, 1);
     
      //Compute rotation matrix
      double rotmat[9];
      euler2rotmat_(phi[i],ssi[i],rot[i],rotmat);
      
      //Apply rotation matrix and translation vector
      rotate_(MAXLIG,3*MAXATOM,rotmat,
      xa[i],ya[i],za[i],
      pivot,i,ieins,x);

    }
    //Compute and print score
    double score;
    deformscore_(TOTMAXATOM,MAXLIG, nlig,
     kai,tyi,rgi,iei,x,iaci,xlai,icop,we, ieins, &score);
    printf("%.5f\n", score); 
    
  }  
}
