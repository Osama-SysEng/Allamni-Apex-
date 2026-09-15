import argparse, json, re
from pathlib import Path
PATTERNS={'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'aws_access_key':re.compile(r'AKIA[0-9A-Z]{16}'),'quoted_secret_assignment':re.compile(r'(?:secret|password|token|api[_-]?key)\s*[:=]\s*[\'\"][^\'\"\s]{12,}[\'\"]',re.I)}
IGNORED={'.git','.venv','venv','node_modules','__pycache__','reports','build','dist'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--output',required=True);a=p.parse_args();root=Path(a.root).resolve();findings=[]
 for f in root.rglob('*'):
  if not f.is_file() or any(x in IGNORED for x in f.parts) or f.name.startswith('.env') or f.stat().st_size>1_000_000:continue
  try:lines=f.read_text(encoding='utf-8').splitlines()
  except UnicodeDecodeError:continue
  for n,line in enumerate(lines,1):
   for rule,pattern in PATTERNS.items():
    if pattern.search(line):findings.append({'rule':rule,'file':str(f.relative_to(root)),'line':n})
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'scanner':'local_secret_heuristic','findings':findings},indent=2),encoding='utf-8');print(json.dumps({'findings':len(findings)}));raise SystemExit(1 if findings else 0)
if __name__=='__main__':main()
