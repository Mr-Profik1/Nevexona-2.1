"""Карантин: изолированная папка (0700), метаданные, восстановление только с подтверждением."""
import hashlib, json, os, shutil, time, uuid

class Quarantine:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        os.makedirs(self.root, mode=0o700, exist_ok=True)
        os.chmod(self.root, 0o700)

    def _meta(self, qid):
        return os.path.join(self.root, qid + ".json")

    def add(self, path, reason="manual"):
        path = os.path.abspath(path)
        if not os.path.isfile(path) or path.startswith(self.root):
            raise ValueError("не файл или уже в карантине")
        if path.startswith(("/usr/", "/bin/", "/sbin/", "/lib", "/boot/", "/etc/")):
            raise PermissionError("системные файлы автоматически не изолируются")
        qid = uuid.uuid4().hex
        dst = os.path.join(self.root, qid + ".bin")
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        shutil.move(path, dst)
        os.chmod(dst, 0o000)
        json.dump({"id": qid, "orig": path, "sha256": h, "reason": reason, "time": time.time()},
                  open(self._meta(qid), "w"))
        return qid

    def list(self):
        return [json.load(open(os.path.join(self.root, f))) for f in sorted(os.listdir(self.root)) if f.endswith(".json")]

    def restore(self, qid, confirmed=False):
        if not confirmed:
            raise PermissionError("восстановление требует подтверждения")
        meta = json.load(open(self._meta(qid)))
        src = os.path.join(self.root, qid + ".bin")
        os.chmod(src, 0o600)
        if os.path.exists(meta["orig"]):
            raise FileExistsError(meta["orig"])
        shutil.move(src, meta["orig"])
        os.remove(self._meta(qid))
        return meta["orig"]
