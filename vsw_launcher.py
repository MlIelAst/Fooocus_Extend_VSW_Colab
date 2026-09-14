# VSW Fooocus_extend Colab Launcher
# Isolierte Python-Umgebung + Fortschritt + Diagnose
import os, sys, time, json, shutil, hashlib, threading, subprocess
from pathlib import Path

PROFILE = "realistic"
THEME = "dark"
TUNNEL = "gradio"
MEMORY_PATCH = True
GOOGLE_DRIVE_OUTPUT = False
USE_LATEST_MAIN = False
FORCE_REBUILD = False

REPO = "https://github.com/shaitanzx/Fooocus_extend.git"
PINNED = "7d32c923c172644023f77243bd7af4183ecb3737"  # v9.3.5
ROOT = Path("/content/Fooocus_extend")
VENV = Path("/content/fooocus_venv")
PY = VENV / "bin/python"
MARKER = VENV / ".vsw_setup.json"
LOG = Path("/content/fooocus_extend_startup.log")
OUT = Path("/content/drive/MyDrive/outputs")
START = time.time()
PHASE = {"name":"Start"}

def elapsed():
    s=int(time.time()-START); return f"{s//60:02d}:{s%60:02d}"

def phase(n, title, eta):
    PHASE["name"]=title
    print(f"\n{'═'*68}\n[{n}/7] {title} | vergangen {elapsed()} | Richtwert {eta}\n{'═'*68}", flush=True)

def run(cmd, cwd=None, heartbeat=20):
    print("$ "+" ".join(map(str,cmd)), flush=True)
    stop=threading.Event()
    def beat():
        while not stop.wait(heartbeat):
            print(f"… läuft weiter | {PHASE['name']} | gesamt {elapsed()}", flush=True)
    t=threading.Thread(target=beat,daemon=True); t.start()
    env=os.environ.copy()
    env.update(PYTHONUNBUFFERED="1",PYTHONNOUSERSITE="1",PIP_DISABLE_PIP_VERSION_CHECK="1")
    with LOG.open("a",encoding="utf-8") as f:
        p=subprocess.Popen([str(x) for x in cmd],cwd=str(cwd) if cwd else None,env=env,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        tail=[]
        for line in p.stdout:
            print(line,end="",flush=True); f.write(line); f.flush()
            tail=(tail+[line.rstrip()])[-60:]
        rc=p.wait()
    stop.set(); t.join(timeout=1)
    if rc:
        print("\nFEHLER – letzte Logzeilen:", flush=True)
        print("\n".join(tail[-30:]), flush=True)
        raise RuntimeError(f"Prozess fehlgeschlagen (Exit {rc}). Vollständiges Log: {LOG}")

def pkg(name):
    r=subprocess.run([str(PY),"-c",f"import importlib.metadata as m;print(m.version('{name}'))"],
                     capture_output=True,text=True)
    return r.stdout.strip() if r.returncode==0 else None

LOG.unlink(missing_ok=True)

phase(1,"System prüfen","< 1 Min.")
print("Python:",sys.version.split()[0],flush=True)
if sys.version_info[:2]!=(3,11):
    raise RuntimeError("Benötigt wird Colab Runtime 2025.07 mit Python 3.11.")
g=subprocess.run(["nvidia-smi","--query-gpu=name,memory.total,driver_version","--format=csv,noheader"],
                 capture_output=True,text=True)
if g.returncode: raise RuntimeError("Keine NVIDIA-GPU erkannt.")
print("GPU:",g.stdout.strip(),flush=True)
free=shutil.disk_usage("/content").free/1024**3
print(f"Freier Speicher: {free:.1f} GB",flush=True)
if free<12: raise RuntimeError("Zu wenig freier Speicher; mindestens ca. 12 GB erforderlich.")

phase(2,"Fooocus-Code bereitstellen","0–2 Min.")
ref="main" if USE_LATEST_MAIN else PINNED
if ROOT.exists() and not (ROOT/".git").exists(): shutil.rmtree(ROOT)
if not ROOT.exists():
    run(["git","clone","--filter=blob:none","--no-checkout",REPO,str(ROOT)])
run(["git","-C",str(ROOT),"fetch","--depth","1","origin",ref])
run(["git","-C",str(ROOT),"checkout","--force","FETCH_HEAD"])
commit=subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()
req=ROOT/"requirements_versions.txt"
req_sha=hashlib.sha256(req.read_bytes()).hexdigest()
print("Fooocus-Commit:",commit,flush=True)

phase(3,"Isolierte Python-Umgebung","0–2 Min.")
if FORCE_REBUILD and VENV.exists(): shutil.rmtree(VENV)
if not PY.exists():
    r=subprocess.run([sys.executable,"-m","venv",str(VENV)],capture_output=True,text=True)
    if r.returncode:
        run([sys.executable,"-m","pip","install","--quiet","virtualenv"])
        run([sys.executable,"-m","virtualenv",str(VENV)])
    run([str(PY),"-m","pip","install","--upgrade","pip","setuptools","wheel"])
else:
    print("VENV bereits vorhanden.",flush=True)

wanted={"python":"3.11","torch":"2.1.0","torchvision":"0.16.0",
        "requirements":req_sha,"commit":commit}
current={}
if MARKER.exists():
    try: current=json.loads(MARKER.read_text())
    except: pass
ready=current==wanted

phase(4,"PyTorch/CUDA in VENV","2–8 Min. beim ersten Start")
if not ready:
    run([str(PY),"-m","pip","install","torch==2.1.0","torchvision==0.16.0",
         "--index-url","https://download.pytorch.org/whl/cu121"])
else:
    print("Übersprungen – bereits eingerichtet.",flush=True)
print("torch:",pkg("torch"),"| torchvision:",pkg("torchvision"),flush=True)

phase(5,"Fooocus-Abhängigkeiten","3–12 Min. beim ersten Start")
if not ready:
    run([str(PY),"-m","pip","install","-r",str(req)],cwd=ROOT)
    run([str(PY),"-m","pip","check"],cwd=ROOT)
    MARKER.write_text(json.dumps(wanted,indent=2))
else:
    print("Übersprungen – bereits eingerichtet.",flush=True)
cuda=subprocess.run([str(PY),"-c",
    "import torch;print(torch.__version__);print(torch.cuda.is_available());"
    "print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')"],
    capture_output=True,text=True)
print(cuda.stdout,flush=True)
if cuda.returncode or "\nTrue\n" not in cuda.stdout:
    raise RuntimeError("Torch in der isolierten Umgebung erkennt CUDA nicht.")

phase(6,"Optionale Dienste","0–2 Min.")
for pattern in ("launch.py","entry_with_update.py","cloudflared tunnel"):
    subprocess.run(["pkill","-f",pattern],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
output=[]
if GOOGLE_DRIVE_OUTPUT:
    from google.colab import drive
    if not Path("/content/drive/MyDrive").exists(): drive.mount("/content/drive",force_remount=False)
    OUT.mkdir(parents=True,exist_ok=True); output=["--output-path",str(OUT)]
else:
    print("Google Drive bleibt getrennt.",flush=True)
if TUNNEL=="cloudflared":
    if not shutil.which("cloudflared"):
        run(["wget","-q","-O","/tmp/cloudflared.deb",
             "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"])
        run(["dpkg","-i","/tmp/cloudflared.deb"])
    run([str(PY),str(ROOT/"patcher_tunel.py")],cwd=ROOT)

phase(7,"Fooocus starten / Modelle laden","2–15+ Min. beim ersten Start")
args=[str(PY),"launch.py","--port","7865"]
if PROFILE in ("realistic","anime"): args+=["--preset",PROFILE]
if THEME=="dark": args+=["--theme","dark"]
if TUNNEL=="gradio": args+=["--share"]
if MEMORY_PATCH: args+=["--always-high-vram","--all-in-fp16"]
args+=output
print("Code-Stand:",commit[:12],"| VENV:",PY,"| Log:",LOG,flush=True)
try:
    run(args,cwd=ROOT,heartbeat=20)
except Exception:
    print("\nVSW-DIAGNOSE",flush=True)
    print("Python:",sys.version.split()[0],"| Commit:",commit,flush=True)
    print("torch:",pkg("torch"),"| torchvision:",pkg("torchvision"),
          "| numpy:",pkg("numpy"),"| pygit2:",pkg("pygit2"),flush=True)
    print(f"Freier Speicher: {shutil.disk_usage('/content').free/1024**3:.1f} GB",flush=True)
    print("Log:",LOG,flush=True)
    raise
