from collections import Counter
import time

class Metrics:
    def __init__(self): self.counters=Counter(); self.started=time.time()
    def inc(self,name:str,n:int=1): self.counters[name]+=n
    def snapshot(self): return {"uptime_seconds":round(time.time()-self.started,2),"counters":dict(self.counters)}

metrics=Metrics()
