#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," AMPA.mod");
    fprintf(stderr," DoubExpSyn.mod");
    fprintf(stderr," Kdr.mod");
    fprintf(stderr," LeakCond.mod");
    fprintf(stderr," NonPlasticSyn.mod");
    fprintf(stderr," SlowCa.mod");
    fprintf(stderr," cad2.mod");
    fprintf(stderr," focalstim.mod");
    fprintf(stderr," glutamate.mod");
    fprintf(stderr," glutamatecad2kca.mod");
    fprintf(stderr," glutnoinact.mod");
    fprintf(stderr," glutnothing.mod");
    fprintf(stderr," h.mod");
    fprintf(stderr," h2.mod");
    fprintf(stderr," hh3.mod");
    fprintf(stderr," ih.mod");
    fprintf(stderr," it2.mod");
    fprintf(stderr," kap.mod");
    fprintf(stderr," kca.mod");
    fprintf(stderr," kcapoint.mod");
    fprintf(stderr," kdf.mod");
    fprintf(stderr," kdr2.mod");
    fprintf(stderr," km.mod");
    fprintf(stderr, "\n");
  }
  _AMPA_reg();
  _DoubExpSyn_reg();
  _Kdr_reg();
  _LeakCond_reg();
  _NonPlasticSyn_reg();
  _SlowCa_reg();
  _cad2_reg();
  _focalstim_reg();
  _glutamate_reg();
  _glutamatecad2kca_reg();
  _glutnoinact_reg();
  _glutnothing_reg();
  _h_reg();
  _h2_reg();
  _hh3_reg();
  _ih_reg();
  _it2_reg();
  _kap_reg();
  _kca_reg();
  _kcapoint_reg();
  _kdf_reg();
  _kdr2_reg();
  _km_reg();
}
