import io, json, os, sys, tempfile, types, unittest, zipfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gaming import platforms
from system import updater
from voice import stt
from ai import assistant

class T(unittest.TestCase):
    def test_platform_install(self):
        with self.assertRaises(PermissionError): platforms.install("steam")
        calls = []
        platforms.install("steam", True, runner=lambda a, **k: (calls.append(a), types.SimpleNamespace(returncode=0))[1])
        self.assertEqual(calls[0][:3], ["pkexec", "dpkg", "--add-architecture"]); self.assertEqual(calls[-1][-1], "steam-installer")
        with self.assertRaises(ValueError): platforms.install("evil; rm", True)
        self.assertEqual(len(platforms.plan("lutris")), 2)
    def test_download_https_only(self):
        with self.assertRaises(ValueError): updater.download("http://x/a.deb", "/tmp/a")
    def test_stt_requires_consent_and_model(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(PermissionError): stt.download(False, t)
            self.assertIn("не загружена", stt.transcribe("x.wav", t)[1])
            buf = io.BytesIO(); z = zipfile.ZipFile(buf, "w"); z.writestr(stt.MODEL["name"] + "/a", "x"); z.close()
            self.assertTrue(stt.download(True, t, opener=lambda u, timeout: io.BytesIO(buf.getvalue())))
        self.assertIn("МБ", stt.info())
    def test_ai_key_and_modes(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "k"); assistant.save_key(" sk-test ", p)
            self.assertEqual(oct(os.stat(p).st_mode)[-3:], "600"); self.assertEqual(assistant.load_key(p), "sk-test")
        with self.assertRaises(PermissionError):
            assistant.ask("hi", "AUTO", consent=lambda m: False, cloud=lambda p, k: "x")
        self.assertEqual(assistant.ask("hi", "AUTO", consent=lambda m: True, key="k", cloud=lambda p, k: "ok"), ("cloud", "ok"))
        with self.assertRaises(RuntimeError): assistant.ask_cloud("hi", None)
        d = {"choices": [{"message": {"content": "ответ"}}]}
        self.assertEqual(assistant.ask_cloud("hi", "k", opener=lambda r, timeout: io.StringIO(json.dumps(d))), "ответ")

if __name__ == "__main__":
    unittest.main()
