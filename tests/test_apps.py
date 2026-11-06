import os, sys, tempfile, unittest, py_compile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, R)
from apps import explorer_core as c

class A(unittest.TestCase):
    def test_human(self):
        self.assertEqual(c.human(500), "500 Б"); self.assertEqual(c.human(2048), "2.0 КБ")
    def test_list_and_trash(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "B")); open(os.path.join(t, "a.txt"), "w").write("xx")
            self.assertEqual([r[0] for r in c.list_dir(t)], ["B", "a.txt"])
            c.delete(os.path.join(t, "a.txt"), os.path.join(t, "Trash")); self.assertFalse(os.path.exists(os.path.join(t, "a.txt")))
    def test_gui_files_compile_and_launchers(self):
        for f in ("explorer", "game_hub", "settings", "control_center", "theme"):
            py_compile.compile(os.path.join(R, "apps", f + ".py"), doraise=True)
        for f in ("nevexona-explorer", "nevexona-gamehub", "nevexona-settings", "nevexona-control-center"):
            p = os.path.join(R, "config/includes.chroot/usr/local/bin", f); self.assertTrue(os.access(p, os.X_OK), f)
            self.assertTrue(os.path.isfile(os.path.join(R, "config/includes.chroot/usr/share/applications", f + ".desktop")), f)

if __name__ == "__main__":
    unittest.main()
