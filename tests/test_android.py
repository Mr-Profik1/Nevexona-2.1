import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gaming import android

class Android(unittest.TestCase):
    def test_launch_validates_and_no_shell(self):
        calls = []
        android.launch("com.mojang.minecraftpe", runner=lambda a, **k: calls.append((a, k)))
        self.assertEqual(calls[0][0], ["waydroid", "app", "launch", "com.mojang.minecraftpe"])
        self.assertFalse(calls[0][1]["shell"])
        with self.assertRaises(ValueError):
            android.launch("a; rm -rf /")
    def test_apk_checks(self):
        with self.assertRaises(ValueError):
            android.install_apk("/etc/passwd")
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "g.apk"); open(f, "w").write("x")
            calls = []
            android.install_apk(f, runner=lambda a, **k: calls.append(a))
            self.assertEqual(calls[0][:3], ["waydroid", "app", "install"])
    def test_requirements_reports_problems(self):
        self.assertIsInstance(android.requirements(), list)

if __name__ == "__main__":
    unittest.main()
