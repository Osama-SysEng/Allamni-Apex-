import argparse, concurrent.futures, json, os, time
from pathlib import Path
from urllib.parse import urlparse
import httpx

def assert_safe_target(url, allow_remote):
    if urlparse(url).hostname not in {'localhost', '127.0.0.1', '::1'} and not allow_remote: raise ValueError('Remote target requires --allow-remote and an approved staging window')

def one(base, path, token):
    started=time.perf_counter()
    try:
        response=httpx.get(base.rstrip('/')+path,headers={'Authorization':f'Bearer {token}'} if token else {},timeout=10)
        return {'status':response.status_code,'latency_ms':round((time.perf_counter()-started)*1000,2)}
    except httpx.HTTPError as exc: return {'status':0,'latency_ms':round((time.perf_counter()-started)*1000,2),'error':type(exc).__name__}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--base-url',default='http://localhost:8002'); parser.add_argument('--path',default='/ready'); parser.add_argument('--requests',type=int,default=25); parser.add_argument('--concurrency',type=int,default=5); parser.add_argument('--allow-remote',action='store_true'); parser.add_argument('--output',default='reports/load/latest.json'); args=parser.parse_args()
    assert_safe_target(args.base_url,args.allow_remote)
    if args.requests < 1 or args.concurrency < 1: parser.error('requests and concurrency must be positive')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool: rows=list(pool.map(lambda _:one(args.base_url,args.path,os.getenv('LOADTEST_BEARER_TOKEN')),range(args.requests)))
    latency=sorted(row['latency_ms'] for row in rows); q=lambda p:latency[min(len(latency)-1,max(0,int(len(latency)*p+.999)-1))]
    report={'target':args.base_url,'path':args.path,'configuration':{'requests':args.requests,'concurrency':args.concurrency},'summary':{'requests':len(rows),'success_rate':round(sum(200<=row['status']<400 for row in rows)/len(rows),4),'p50_ms':q(.5),'p95_ms':q(.95),'p99_ms':q(.99),'max_ms':max(latency)}}
    output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2),encoding='utf-8'); print(json.dumps(report['summary'],indent=2))
if __name__=='__main__': main()
