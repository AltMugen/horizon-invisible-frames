#!/usr/bin/env python3
"""Package, or apply/build the exact committed Horizon revision. No player data is used."""
import argparse,hashlib,json,os,subprocess,tarfile,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('action',choices=['package','check','build']);p.add_argument('--horizon',type=Path);p.add_argument('--mixins-cli',type=Path);p.add_argument('--target-dir',type=Path);p.add_argument('--work',type=Path);p.add_argument('--out',type=Path,default=ROOT/'dist');a=p.parse_args()
meta=json.loads((ROOT/'horizon-native.json').read_text());mod=meta['id']
if a.action=='package':
 a.out.mkdir(parents=True,exist_ok=True);out=a.out/f'{mod}-{meta["version"]}.hnmod'
 files={'horizon-native.json':(ROOT/'horizon-native.json').read_bytes()}
 for src in (ROOT/'mixins'/mod).rglob('*'):
  if src.is_file() and (src.suffix in ('.rs','.toml') or 'data' in src.parts):files[str(src.relative_to(ROOT))]=src.read_bytes()
 for name in ['LICENSE','README.md','VALIDATION.md']:
  if (ROOT/name).exists():files[f'mixins/{mod}/'+('README-VALIDATION.md' if name=='VALIDATION.md' else name)]=(ROOT/name).read_bytes()
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for name,data in sorted(files.items()):
   info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
 print(json.dumps({'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}));raise SystemExit
if not all([a.horizon,a.mixins_cli,a.target_dir]):p.error('--horizon, --mixins-cli and --target-dir are required')
with tempfile.TemporaryDirectory(prefix='altcraft-native-',dir=a.work) as d:
 original=Path(d)/'original';original.mkdir()
 proc=subprocess.Popen(['git','-C',str(a.horizon.resolve()),'archive',meta['horizon']],stdout=subprocess.PIPE)
 with tarfile.open(fileobj=proc.stdout,mode='r|') as tar:tar.extractall(original,filter='data')
 proc.stdout.close()
 if proc.wait():raise SystemExit('git archive failed')
 for file in original.rglob('*'):
  if file.is_symlink():content=file.read_bytes();file.unlink();file.write_bytes(content)
 (original/'.horizon-revision').write_text(meta['horizon']+'\n')
 stage=Path(d)/'stage'
 subprocess.run([str(a.mixins_cli.resolve()),'apply','--workspace',str(original),'--mods',str(ROOT/'mixins'),'--out',str(stage)],check=True)
 env=dict(os.environ,CARGO_TARGET_DIR=str(a.target_dir.resolve()))
 command=['cargo','check' if a.action=='check' else 'build','--locked','--offline','-p','horizon-client','--bin','horizon-client']
 if a.action=='build':command+=['--profile','fast']
 subprocess.run(command,cwd=stage,env=env,check=True)
