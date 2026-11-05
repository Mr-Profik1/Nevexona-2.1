import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from voice import intents
from security.quarantine import Quarantine
from system import backup, monitor

class Voice(unittest.TestCase):
    def test_known(self):
        self.assertEqual(intents.parse("Открой браузер").argv, ("firefox-esr",))
        self.assertEqual(intents.parse("Увеличь громкость.").name, "vol_up")
    def test_no_arbitrary_shell(self):
        for t in ["rm -rf /", "открой браузер; rm -rf /", "открой папку ../../etc", "$(reboot)", "выключи компьютер && ls"]:
            self.assertIsNone(intents.parse(t), t)
    def test_dangerous_needs_confirm(self):
        i = intents.parse("выключи компьютер")
        self.assertTrue(i.confirm and i.admin)
        with self.assertRaises(PermissionError):
            intents.run(i)
        calls = []
        intents.run(i, confirmed=True, runner=lambda a, **k: calls.append((a, k)))
        self.assertEqual(calls[0][0], ["systemctl", "poweroff"])
        self.assertFalse(calls[0][1]["shell"])

class Quar(unittest.TestCase):
    def test_cycle(self):
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "bad.txt"); open(f, "w").write("x")
            q = Quarantine(os.path.join(t, "q"))
            self.assertEqual(oct(os.stat(q.root).st_mode)[-3:], "700")
            qid = q.add(f)
            self.assertFalse(os.path.exists(f))
            self.assertEqual(len(q.list()), 1)
            with self.assertRaises(PermissionError):
                q.restore(qid)
            q.restore(qid, confirmed=True)
            self.assertTrue(os.path.exists(f))
    def test_system_file_refused(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(PermissionError):
                Quarantine(t).add("/etc/passwd")

class Backup(unittest.TestCase):
    def test_cycle(self):
        with tempfile.TemporaryDirectory() as t:
            src = os.path.join(t, "docs"); os.makedirs(src)
            open(os.path.join(src, "a.txt"), "w").write("hello")
            dest = os.path.join(t, "bk")
            backup.backup([src], dest)
            self.assertEqual(backup.verify(dest), [])
            open(os.path.join(dest, "files", "docs", "a.txt"), "w").write("broken")
            self.assertEqual(backup.verify(dest), ["docs/a.txt"])

class Mon(unittest.TestCase):
    def test_values(self):
        self.assertGreater(monitor.disk()["total"], 0)

if __name__ == "__main__":
    unittest.main()
