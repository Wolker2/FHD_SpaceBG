#!/usr/bin/env python3
"""Verify original-byte config recovery and accurately report absent artwork."""
from pathlib import Path
import argparse,json,platform,shutil,sys,tempfile,zlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,hashes,load,audit,require_complete
from dat_codec import decode,encode
def verify():
    checks=[]
    def check(condition,label):
        assert condition,label;checks.append(label)
    with tempfile.TemporaryDirectory() as tmp:
        clean=Path(tmp);shutil.copytree(ROOT/'source',clean/'source');files=build(clean)
    check(hashes(files)==load(ROOT/'original-file-sha256.json'),'Both supplied files rebuild with original SHA-256 from editable source inputs')
    check(encode(decode(files['CFG/CacheData.dat'],'cachedata'))==files['CFG/CacheData.dat'],'DAT checksum, decompression and complete typed parse/encode roundtrip')
    check(files['ModuleInfo.txt'][:2]==b'\xff\xfe','Original UTF-16LE BOM retained')
    check(files['ModuleInfo.txt'][2:].decode('utf-16le')==(ROOT/'source/ModuleInfo.txt').read_bytes().decode('utf-8'),'Metadata encoding and line endings preserved')
    report=audit()
    check(len(report['references'])==33 and report['missing_background_files']==33,'All 33 references audited; all 33 GAI assets absent from upload')
    check(not report['full_mod_ready'],'Incomplete source upload is not reported as a complete mod')
    try:require_complete(report)
    except ValueError:blocked=True
    else:blocked=False
    check(blocked,'Strict completeness gate refuses a full-resource build')
    return {'source_reconstruction':'passed','checks_passed':len(checks),'checks':checks,'resource_completeness':report,
            'runtime_sha256':hashes(files),'live_game_executed':False,'environment':{'python':platform.python_version(),'zlib':zlib.ZLIB_RUNTIME_VERSION}}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);a=p.parse_args();r=verify()
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_reconstruction':r['source_reconstruction'],'checks_passed':r['checks_passed'],'full_mod_ready':r['resource_completeness']['full_mod_ready'],'missing_background_files':33},indent=2))
