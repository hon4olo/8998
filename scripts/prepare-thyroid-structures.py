#!/usr/bin/env python3
"""Extract real PDB/CCD coordinates, keeping provenance and chemical mapping auditable."""
import pathlib,json,shlex,hashlib,numpy as np
root=pathlib.Path('projects/voice-quality/assets/structures')
def ccd(id):
 lines=(root/(id+'.cif')).read_text().splitlines();out={}
 for kind in ['atom','bond']:
  prefix='_chem_comp_'+kind+'.';heads=[l for l in lines if l.startswith(prefix)]
  start=lines.index(heads[-1])+1;rows=[]
  for l in lines[start:]:
   if l.startswith('#'):break
   vals=shlex.split(l);rows.append(dict(zip([x.split('.')[1].strip() for x in heads],vals)))
  out[kind]=rows
 return out
three=ccd('T3');four=ccd('T44');lines=(root/'2H77.pdb').read_text().splitlines()
lig={};atoms=[];res={};helices=[]
for l in lines:
 if l.startswith('HELIX'):helices.append([int(l[21:25]),int(l[33:37])])
 if l.startswith(('ATOM  ','HETATM')) and l[21]=='A' and l[16] in [' ','A']:
  pos=[float(l[30:38]),float(l[38:46]),float(l[46:54])];name=l[12:16].strip();num=int(l[22:26]);element=l[76:78].strip()
  if l[17:20].strip()=='T3':lig[name]=pos
  elif l.startswith('ATOM') or l[17:20]=='CAS':
   # CAS is an experimentally modified cysteine: retain backbone, exclude arsenic adduct from surface.
   if element not in ['H','AS'] and not (l[17:20]=='CAS' and name in ['CE1','CE2']):atoms.append({'p':pos,'e':element,'res':num})
   res.setdefault(num,{})[name]=pos
center=np.mean(list(lig.values()),axis=0)
# PCA on ligand ring skeleton gives repeatable, useful frontal orientation; determinant preserves handedness.
pts=np.array([lig[k] for k in ['C1','C3','C5','C7','C9','C11','C2','C4','C6','C8','C10','C12']]);_,_,basis=np.linalg.svd(pts-pts.mean(0));basis=basis.T
if np.linalg.det(basis)<0:basis[:,2]*=-1
# x major axis, y second, z front.
def transform(p):return np.round((np.array(p)-center)@basis,5).tolist()
map4={'C1':'C1','C2':'C3','C3':'C5','C4':'C7','C5':'C9','C6':'C11','C7':'C13','CA':'CA','C':'C','N':'N','O':'O','OXT':'OXT',"C1'":'C2',"C2'":'C4',"C3'":'C6',"C4'":'C8',"C5'":'C10',"C6'":'C12','O4':'O2',"O4'":'O1','I3':'I1',"I3'":'I2','I5':'I3'}
a4={a['atom_id']:a for a in four['atom'] if a['type_symbol']!='H'}
def ideal(a):return np.array([float(a['pdbx_model_Cartn_'+s+'_ideal']) for s in 'xyz'])
x=np.array([ideal(a4[k]) for k in map4]);y=np.array([lig[v] for v in map4.values()]);xc=x.mean(0);yc=y.mean(0);u,_,vt=np.linalg.svd((x-xc).T@(y-yc));rot=u@np.diag([1,1,np.linalg.det(u@vt)])@vt
fourAtoms=[{'id':map4.get(k,k),'e':a['type_symbol'],'p':transform((ideal(a)-xc)@rot+yc)} for k,a in a4.items()]
threeAtoms=[{'id':k,'e':next(a['type_symbol'] for a in three['atom'] if a['atom_id']==k),'p':transform(v)} for k,v in lig.items()]
def bonds(data,mapping):return [[mapping.get(a['atom_id_1'],a['atom_id_1']),mapping.get(a['atom_id_2'],a['atom_id_2']),a['value_order']] for a in data['bond'] if not a['atom_id_1'].startswith('H') and not a['atom_id_2'].startswith('H')]
backbone=[]
for n,r in sorted(res.items()):
 if 'CA' in r:backbone.append({'res':n,'p':transform(r['CA']),'helix':any(a<=n<=b for a,b in helices)})
out={'source':{'receptor':'2H77 chain A, human THRA ligand-binding domain, X-ray 2.33 angstrom','t3':'2H77 bound coordinates + CCD T3 bonds','t4':'CCD T44 ideal conformer, rigid Kabsch aligned; not experimentally observed conversion','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*') if p.suffix in ['.pdb','.cif']}},'t3':{'atoms':threeAtoms,'bonds':bonds(three,{})},'t4':{'atoms':fourAtoms,'bonds':bonds(four,map4)},'backbone':backbone,'proteinAtoms':[dict(a,p=transform(a['p'])) for a in atoms]}
(root/'geometry.json').write_text(json.dumps(out,separators=(',',':')))
print('T3/T4 heavy atoms:',len(threeAtoms),len(fourAtoms),'CA:',len(backbone),'surface atoms:',len(atoms))
assert len(threeAtoms)==23 and len(fourAtoms)==24
assert sum(a['e']=='I' for a in threeAtoms)==3 and sum(a['e']=='I' for a in fourAtoms)==4
assert len(backbone)>240
