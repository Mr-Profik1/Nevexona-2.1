import hashlib, io, json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from system import updater

class Upd(unittest.TestCase):
    def test_newer(self):
        self.assertTrue(updater.newer("0.3.0", "0.2.0"))
        self.assertFalse(updater.newer("v0.2.0", "0.2.0"))
    def test_fetch(self):
        data = {"tag_name": "v0.3.0", "assets": [
            {"name": "n.deb", "browser_download_url": "u1"}, {"name": "n.deb.sha256", "browser_download_url": "u2"}]}
        r = updater.fetch_latest(opener=lambda u, timeout: io.StringIO(json.dumps(data)))
        self.assertEqual(r["version"], "0.3.0")
        self.assertIsNone(updater.fetch_latest(opener=lambda u, timeout: io.StringIO('{"tag_name":"v1","assets":[]}')))
    def test_verify_and_confirm(self):
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "a.deb"); open(f, "wb").write(b"abc")
            good = hashlib.sha256(b"abc").hexdigest()
            self.assertTrue(updater.verify(f, good + "  a.deb"))
            with self.assertRaises(ValueError):
                updater.verify(f, "0" * 64)
            with self.assertRaises(PermissionError):
                updater.install(f)
            calls = []
            updater.install(f, confirmed=True, runner=lambda a, **k: calls.append(a))
            self.assertEqual(calls[0][:3], ["pkexec", "apt", "install"])

if __name__ == "__main__":
    unittest.main()
