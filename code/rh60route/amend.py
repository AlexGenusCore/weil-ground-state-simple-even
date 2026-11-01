"""Append-only amendment log (AUDIT F5). One JSON line per entry, written at once with the UTC time of the write, the md5 of
each named file at that moment, and the sha256 of the whole log before this entry (a hash chain: editing or deleting an earlier
entry breaks every later link). Each certifier run records the log's sha256 at its start (RH60_AMEND), which pins the log.
  python amend.py LOG "text" [file ...]     append one entry
  python amend.py LOG --verify               check the chain"""
import hashlib, json, os, sys, time

log = sys.argv[1]
data = open(log, "rb").read() if os.path.exists(log) else b""
if sys.argv[2] == "--verify":
    pos = 0; lines = data.splitlines(keepends=True)
    for i, line in enumerate(lines):
        assert json.loads(line)["prev_sha256"] == hashlib.sha256(data[:pos]).hexdigest(), f"chain broken at entry {i + 1}"
        pos += len(line)
    print(f"chain OK, {len(lines)} entries, sha256 {hashlib.sha256(data).hexdigest()}")
else:
    md5 = lambda f: hashlib.md5(open(f, "rb").read()).hexdigest()
    e = dict(n=data.count(b"\n") + 1, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), prev_sha256=hashlib.sha256(data).hexdigest(),
             md5={f: md5(f) for f in sys.argv[3:]}, text=sys.argv[2])
    with open(log, "ab") as f: f.write((json.dumps(e, ensure_ascii=False) + "\n").encode())
    print(json.dumps(e, ensure_ascii=False))
