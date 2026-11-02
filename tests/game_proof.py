"""Real input/packet check with isolated game homes. No real worlds/settings touched."""
import argparse,json,os,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--ctl',required=True);p.add_argument('--resources',required=True);p.add_argument('--registry-tools',required=True);p.add_argument('--out',required=True);a=p.parse_args()
sys.path.insert(0,a.registry_tools);from game import Game
os.environ['HORIZON_TELEMETRY_URL']='off';os.environ['HORIZON_PLAYER_NAME']='FrameProof'
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);results=[]
# horizon-ctl key bypasses physical rebinding; do not claim physical-key coverage here.
for key in ['key.keyboard.left.shift']:
 with Game(a.ctl,a.resources,str(out/key),files={'options.txt':'key_key.sneak:'+key+'\n'}) as g:
  def cmd(line):
   v=g.run('command',line);print(key,line,v,flush=True);results.append({'binding':key,'command':line,'reply':v});(out/'results.json').write_text(json.dumps(results,indent=2));return json.dumps(v)
  for line in ['time set noon','fill -3 99 -3 3 99 5 minecraft:stone','fill -1 100 3 1 102 3 minecraft:stone','tp @s 0.5 100 0.5 0 0','summon minecraft:item_frame 0.5 101.5 2.97 {Facing:2b,block_pos:[I;0,101,2],Item:{id:"minecraft:diamond",count:1}}']:cmd(line)
  g.run('look-at','0.5','101.5','2.96875');time.sleep(.2)
  g.run('mouse','right','click');time.sleep(.2);assert '0b' in cmd('data get entity @e[type=minecraft:item_frame,limit=1] Invisible')
  g.run('key',key,'down');time.sleep(.2)
  g.run('look-at','0.5','101.5','2.96875');g.run('mouse','right','click');time.sleep(.2)
  assert '1b' in cmd('data get entity @e[type=minecraft:item_frame,limit=1] Invisible')
  assert '1b' in cmd('data get entity @e[type=minecraft:item_frame,limit=1] Fixed')
  g.run('mouse','right','click');time.sleep(.2)
  assert '0b' in cmd('data get entity @e[type=minecraft:item_frame,limit=1] Invisible')
  assert '0b' in cmd('data get entity @e[type=minecraft:item_frame,limit=1] Fixed')
  g.run('release')
print('PASS: normal click does not toggle; server sneak toggles hidden/fixed on and off')
