import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apps import panels

class Panels(unittest.TestCase):
    def test_monitor(self): self.assertIn("ОЗУ", panels.monitor_text())
    def test_drivers(self):
        rows = panels.drivers_rows(scan=lambda: [{"vendor": "V", "name": "N", "driver": None, "status": "Нет драйвера", "firmware_pkg": None}])
        self.assertEqual(rows[0][2], "—")
        def boom(): raise FileNotFoundError
        self.assertEqual(panels.drivers_rows(scan=boom), [])
    def test_voice(self):
        self.assertEqual(panels.voice_preview("rm -rf /")[1], None)
        self.assertIn("подтверждение", panels.voice_preview("выключи компьютер")[0])
    def test_games_quarantine(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(panels.games_rows(os.path.join(t, "g.json"), steam_root=t), [])
            self.assertEqual(panels.quarantine_rows(os.path.join(t, "q")), [])
    def test_update_offline(self):
        def bad(u, timeout): raise OSError("нет сети")
        self.assertIn("Нет связи", panels.update_status(opener=bad))
    def test_gui_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(os.path.dirname(panels.__file__), "control_center.py"), doraise=True)

if __name__ == "__main__":
    unittest.main()
