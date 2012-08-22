/* Created by Language version: 6.2.0 */
/* NOT VECTORIZED */
#include <stdio.h>
#include <math.h>
#include "scoplib.h"
#undef PI
 
#include "md1redef.h"
#include "section.h"
#include "md2redef.h"

#if METHOD3
extern int _method3;
#endif

#undef exp
#define exp hoc_Exp
extern double hoc_Exp();
 
#define _threadargscomma_ /**/
#define _threadargs_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gmax _p[0]
#define e _p[1]
#define ntar _p[2]
#define gnmda _p[3]
#define inmda _p[4]
#define i _p[5]
#define local_v _p[6]
#define ca_influx _p[7]
#define g _p[8]
#define A _p[9]
#define B _p[10]
#define h _p[11]
#define ca _p[12]
#define gh _p[13]
#define drive_channel _p[14]
#define Dg _p[15]
#define DA _p[16]
#define DB _p[17]
#define Dh _p[18]
#define Dca _p[19]
#define _g _p[20]
#define _tsav _p[21]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern int nrn_get_mechtype();
 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 static _hoc_setdata(_vptr) void* _vptr; { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 /* connect user functions to hoc names */
 static IntFunc hoc_intfunc[] = {
 0,0
};
 static struct Member_func {
	char* _name; double (*_member)();} _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 0, 0
};
 /* declare global and static user variables */
#define cainf cainf_glutamatecad2
 double cainf = 0.0001;
#define cah cah_glutamatecad2
 double cah = 8;
#define depth depth_glutamatecad2
 double depth = 0.1;
#define gama gama_glutamatecad2
 double gama = 0.08;
#define n n_glutamatecad2
 double n = 0.3;
#define scale scale_glutamatecad2
 double scale = 1;
#define taur taur_glutamatecad2
 double taur = 80;
#define tauh tauh_glutamatecad2
 double tauh = 1000;
#define tau_ampa tau_ampa_glutamatecad2
 double tau_ampa = 1;
#define tau2 tau2_glutamatecad2
 double tau2 = 3;
#define tau1 tau1_glutamatecad2
 double tau1 = 70;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "tau1_glutamatecad2", "ms",
 "tau_ampa_glutamatecad2", "ms",
 "gama_glutamatecad2", "/mV",
 "cah_glutamatecad2", "/ms",
 "tauh_glutamatecad2", "/ms",
 "depth_glutamatecad2", "um",
 "taur_glutamatecad2", "ms",
 "cainf_glutamatecad2", "mM",
 "gmax", "nS",
 "e", "mV",
 "A", "nS",
 "B", "nS",
 "h", "nS",
 "ca", "mM",
 "i", "nA",
 "local_v", "mV",
 "ca_influx", "mA",
 0,0
};
 static double A0 = 0;
 static double B0 = 0;
 static double ca0 = 0;
 static double delta_t = 0.01;
 static double g0 = 0;
 static double h0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "tau1_glutamatecad2", &tau1_glutamatecad2,
 "tau2_glutamatecad2", &tau2_glutamatecad2,
 "tau_ampa_glutamatecad2", &tau_ampa_glutamatecad2,
 "n_glutamatecad2", &n_glutamatecad2,
 "gama_glutamatecad2", &gama_glutamatecad2,
 "cah_glutamatecad2", &cah_glutamatecad2,
 "tauh_glutamatecad2", &tauh_glutamatecad2,
 "depth_glutamatecad2", &depth_glutamatecad2,
 "taur_glutamatecad2", &taur_glutamatecad2,
 "cainf_glutamatecad2", &cainf_glutamatecad2,
 "scale_glutamatecad2", &scale_glutamatecad2,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(), nrn_init(), nrn_state();
 static void nrn_cur(), nrn_jacob();
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   destroy_point_process(_vptr);
}
 
static int _ode_count(), _ode_map(), _ode_spec(), _ode_matsol();
 
#define _cvode_ieq _ppvar[2]._i
 /* connect range variables in _p that hoc is supposed to know about */
 static char *_mechanism[] = {
 "6.2.0",
"glutamatecad2",
 "gmax",
 "e",
 "ntar",
 "gnmda",
 "inmda",
 0,
 "i",
 "local_v",
 "ca_influx",
 0,
 "g",
 "A",
 "B",
 "h",
 "ca",
 0,
 0};
 
static void nrn_alloc(_prop)
	Prop *_prop;
{
	Prop *prop_ion, *need_memb();
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 22, _prop);
 	/*initialize range parameters*/
 	gmax = 1;
 	e = 0;
 	ntar = 1;
 	gnmda = 0;
 	inmda = 0;
  }
 	_prop->param = _p;
 	_prop->param_size = 22;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static _net_receive();
 typedef (*_Pfrv)();
 extern _Pfrv* pnt_receive;
 extern short* pnt_receive_size;
 _glutamatecad2_reg() {
	int _vectorized = 0;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func,
	 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
  hoc_register_dparam_size(_mechtype, 3);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 2;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 glutamatecad2 /Users/danielruedt/PhD/simulations/LarkumEtAl2009_template_ratecoding/umac/glutamatecad2.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double F = 96480.0;
 static double R = 8.314;
 static double FARADAY = 96485.3;
static int _reset;
static char *modelname = "combination of NMDA synapse, Ca pump and KCa";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(), _ode_matsol1();
 extern int state_discon_flag_;
 static int _slist1[5], _dlist1[5];
 static int state();
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   Dg = - g / tau_ampa ;
   DA = - A / tau1 ;
   DB = - B / tau2 ;
   Dh = ( cah * ca - h ) / tauh ;
   drive_channel = - ( 10000.0 ) * ca_influx / ( 2.0 * FARADAY * depth ) ;
   if ( drive_channel <= 0. ) {
     drive_channel = 0. ;
     }
   Dca = drive_channel * 72.2 * scale + ( cainf - ca ) / taur ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 Dg = Dg  / (1. - dt*( ( - 1.0 ) / tau_ampa )) ;
 DA = DA  / (1. - dt*( ( - 1.0 ) / tau1 )) ;
 DB = DB  / (1. - dt*( ( - 1.0 ) / tau2 )) ;
 Dh = Dh  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tauh )) ;
 drive_channel = - ( 10000.0 ) * ca_influx / ( 2.0 * FARADAY * depth ) ;
 if ( drive_channel <= 0. ) {
   drive_channel = 0. ;
   }
 Dca = Dca  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taur )) ;
}
 /*END CVODE*/
 static int state () {_reset=0;
 {
    g = g + (1. - exp(dt*(( - 1.0 ) / tau_ampa)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_ampa ) - g) ;
    A = A + (1. - exp(dt*(( - 1.0 ) / tau1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau1 ) - A) ;
    B = B + (1. - exp(dt*(( - 1.0 ) / tau2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau2 ) - B) ;
    h = h + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tauh)))*(- ( ( ( (cah)*(ca) ) ) / tauh ) / ( ( ( ( - 1.0) ) ) / tauh ) - h) ;
   drive_channel = - ( 10000.0 ) * ca_influx / ( 2.0 * FARADAY * depth ) ;
   if ( drive_channel <= 0. ) {
     drive_channel = 0. ;
     }
    ca = ca + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taur)))*(- ( ((drive_channel)*(72.2))*(scale) + ( ( cainf ) ) / taur ) / ( ( ( ( - 1.0) ) ) / taur ) - ca) ;
   }
  return 0;
}
 
static _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{    _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
   state_discontinuity ( _cvode_ieq + 1, & A , A + gmax ) ;
   state_discontinuity ( _cvode_ieq + 2, & B , B + gmax ) ;
   state_discontinuity ( _cvode_ieq + 0, & g , g + gmax / ntar ) ;
   _args[1] = t ;
   } }
 
static int _ode_count(_type) int _type;{ return 5;}
 
static int _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 ();
 }}
 
static int _ode_map(_ieq, _pv, _pvdot, _pp, _ppd, _atol, _type) int _ieq, _type; double** _pv, **_pvdot, *_pp, *_atol; Datum* _ppd; { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 5; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static int _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol1 ();
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  A = A0;
  B = B0;
  ca = ca0;
  g = g0;
  h = h0;
 {
   g = 0.0 ;
   A = 0.0 ;
   B = 0.0 ;
   h = 0.0 ;
   ca = cainf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gnmda = ( A - B ) / ( 1.0 + n * exp ( - gama * v ) ) ;
   gh = ( exp ( - h ) ) ;
   inmda = ( 1e-3 ) * gnmda * gh * ( v - e ) ;
   ca_influx = ( inmda / 10.0 ) ;
   i = ( 1e-3 ) * g * ( v - e ) + inmda + inmda / 10.0 ;
   local_v = v ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_v + .001);
 	{ state_discon_flag_ = 1; _rhs = _nrn_current(_v); state_discon_flag_ = 0;
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
 double _break, _save;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _break = t + .5*dt; _save = t;
 v=_v;
{
 { {
 for (; t < _break; t += dt) {
 error =  state();
 if(error){fprintf(stderr,"at line 109 in file glutamatecad2.mod:\n	\n"); nrn_complain(_p); abort_run(error);}
 
}}
 t = _save;
 }}}

}

static terminal(){}

static _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(g) - _p;  _dlist1[0] = &(Dg) - _p;
 _slist1[1] = &(A) - _p;  _dlist1[1] = &(DA) - _p;
 _slist1[2] = &(B) - _p;  _dlist1[2] = &(DB) - _p;
 _slist1[3] = &(h) - _p;  _dlist1[3] = &(Dh) - _p;
 _slist1[4] = &(ca) - _p;  _dlist1[4] = &(Dca) - _p;
_first = 0;
}
