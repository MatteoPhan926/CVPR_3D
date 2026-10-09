from pathlib import Path
import urllib.request, urllib.error, json, hashlib, concurrent.futures, datetime
ROOT=Path(__file__).parent
SOURCES={
"zerogpu_doc":"https://huggingface.co/docs/hub/spaces-zerogpu",
"zerogpu_doc_raw":"https://raw.githubusercontent.com/huggingface/hub-docs/main/docs/hub/spaces-zerogpu.md",
"tokens_doc":"https://huggingface.co/docs/hub/security-tokens",
"space_api_doc":"https://huggingface.co/docs/hub/spaces-api",
"space_readme":"https://huggingface.co/spaces/microsoft/TRELLIS.2/raw/main/README.md",
"space_requirements":"https://huggingface.co/spaces/microsoft/TRELLIS.2/raw/main/requirements.txt",
"space_app_current":"https://huggingface.co/spaces/microsoft/TRELLIS.2/raw/main/app.py",
"space_meta":"https://huggingface.co/api/spaces/microsoft/TRELLIS.2",
"spaces_pypi":"https://pypi.org/pypi/spaces/json",
}
def fetch(item):
 name,url=item
 rec={"name":name,"url":url,"requested_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"method":"GET","authentication":"none; urllib explicit User-Agent only"}
 try:
  request=urllib.request.Request(url,headers={"User-Agent":"Codex-read-only-route-research"})
  with urllib.request.urlopen(request,timeout=40) as r:
   body=r.read(); rec.update(status=r.status,final_url=r.url,response_headers=dict(r.headers),size=len(body),sha256=hashlib.sha256(body).hexdigest())
  filename=name+('.json' if name in ['space_meta','spaces_pypi'] else '.txt')
  (ROOT/filename).write_bytes(body);rec['snapshot']=filename
 except urllib.error.HTTPError as e:
  body=e.read();filename=name+'.error.txt';(ROOT/filename).write_bytes(body)
  rec.update(status=e.code,error=str(e),size=len(body),sha256=hashlib.sha256(body).hexdigest(),snapshot=filename)
 except Exception as e:rec.update(error=repr(e))
 rec['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (ROOT/(name+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
 return {k:v for k,v in rec.items() if k!='response_headers'}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
  for result in pool.map(fetch,SOURCES.items()):print(json.dumps(result))
