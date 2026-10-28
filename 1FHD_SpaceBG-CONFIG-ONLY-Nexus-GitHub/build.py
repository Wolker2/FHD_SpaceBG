#!/usr/bin/env python3
"""Rebuild only the two supplied SpaceBG files. This upload has no artwork."""
from pathlib import Path
import argparse,hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from dat_codec import encode as encode_dat
PREFIX='Mods/FHD_MODS/FHD_SpaceBG/'
def load(path):return json.loads(Path(path).read_text('utf-8'))
def hashes(files):return {n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())}
def build(root=ROOT):
    source=Path(root)/'source'
    return {'CFG/CacheData.dat':encode_dat(load(source/'CacheData.json')),
            'ModuleInfo.txt':b'\xff\xfe'+(source/'ModuleInfo.txt').read_bytes().decode('utf-8').encode('utf-16le')}
def references(block,prefix=''):
    for e in block['entries']:
        name=prefix+e['name']
        if e['kind']=='block':yield from references(e['value'],name+'.')
        else:yield name,e['value']
def audit(root=ROOT):
    files=build(root);rows=[]
    for alias,target in references(load(Path(root)/'source/CacheData.json')['root']):
        name=target.replace('\\','/').removeprefix(PREFIX)
        rows.append({'alias':alias,'target':target,'relative_path':name,'included_in_supplied_payload':name in files})
    missing=[r for r in rows if not r['included_in_supplied_payload']]
    return {'status':'incomplete'if missing else'complete','full_mod_ready':not missing,'references':rows,
            'missing_background_files':len(missing),'optional_fon_folder_supplied':False}
def require_complete(report):
    if not report['full_mod_ready']:raise ValueError(str(report['missing_background_files'])+' referenced backgrounds are missing; this is a config-only source package')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify-original',action='store_true');p.add_argument('--require-resources',action='store_true')
    p.add_argument('--output',type=Path,default=ROOT/'dist/FHD_SpaceBG-CONFIG-ONLY.zip');a=p.parse_args();files=build();report=audit()
    if a.verify_original and hashes(files)!=load(ROOT/'original-file-sha256.json'):raise SystemExit('Original file hashes differ')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    (a.output.parent/'resource-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if a.require_resources:
        try:require_complete(report)
        except ValueError as e:raise SystemExit(str(e))
    with zipfile.ZipFile(a.output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(PREFIX+name,(2026,1,1,0,0,0));info.external_attr=0o644<<16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'rebuilt_files':len(files),'original_bytes_verified':a.verify_original,'full_mod_ready':report['full_mod_ready'],'missing_background_files':report['missing_background_files'],'output':str(a.output)},indent=2))
if __name__=='__main__':main()
