import os, sys, tempfile, types, unittest, py_compile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, R)
from system import schedule, monitors, backup_cli, backup
from security import integrity, scanner
from gaming import proton
from voice import session

XR = "Screen 0: minimum 8 x 8\nHDMI-1 connected 1920x1080+0+0\n   1920x1080     60.00*+\n   1280x720      60.00\nVGA-1 disconnected\n"

class F(unittest.TestCase):
    def test_schedule(self):
        s, t = schedule.make_units(["/home/u/Docs"], "/mnt/bk", "weekly"); self.assertIn("OnCalendar=weekly", t); self.assertIn("backup_cli.py", s)
        with self.assertRaises(ValueError): schedule.make_units(["/x\nExecStart=evil"], "/b")
        with self.assertRaises(ValueError): schedule.make_units(["rel"], "/b")
        with self.assertRaises(ValueError): schedule.make_units(["/a"], "/b", "minutely")
        with tempfile.TemporaryDirectory() as h: self.assertTrue(os.path.isfile(os.path.join(schedule.install_units(["/a"], "/b", home=h), "nevexona-backup.timer")))
    def test_backup_cli(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "s")); open(os.path.join(t, "s", "a"), "w").write("1")
            self.assertEqual(backup_cli.main(["x", os.path.join(t, "d"), os.path.join(t, "s")]), 0); self.assertEqual(backup_cli.main(["x"]), 2)
    def test_integrity(self):
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "f"); open(f, "w").write("a"); b = integrity.baseline([f, "/no/such"]); self.assertEqual(b["skipped"], ["/no/such"])
            open(f, "w").write("b"); self.assertEqual(integrity.compare(b)["changed"], [f]); os.remove(f); self.assertEqual(integrity.compare(b)["missing"], [f])
            ab = os.path.join(t, "ab"); open(ab, "w").write("firefox &\n# c\n"); self.assertEqual(integrity.autostart([], ab)[0]["exec"], "firefox")
    def test_usb(self): self.assertEqual(scanner.usb_mounts("a /media/u/USB\\040X ext4 0 0\nb / ext4 0 0\n"), ["/media/u/USB X"])
    def test_monitors(self):
        m = monitors.parse_xrandr(XR); self.assertEqual((m[0]["current"], m[1]["connected"]), ("1920x1080", False))
        self.assertEqual(monitors.set_mode("HDMI-1", "1280x720")[-1], "1280x720")
        with self.assertRaises(ValueError): monitors.set_mode("HDMI-1; rm", "1x1")
    def test_proton(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "compatibilitytools.d", "GE-Proton9-1")); os.makedirs(os.path.join(t, "steamapps", "common", "Proton 9.0"))
            self.assertEqual(proton.versions(t), ["GE-Proton9-1", "Proton 9.0"])
            with self.assertRaises(FileNotFoundError): proton.backup_saves(["/no"], os.path.join(t, "bk"))
    def test_voice_session(self):
        r = session.listen_once("/tmp/x.wav", recorder=lambda p, s: None, transcriber=lambda p: ("выключи компьютер", "ok"))
        self.assertTrue(r["needs_confirm"]); self.assertEqual(session.listen_once("/tmp/x.wav", recorder=lambda p, s: None, transcriber=lambda p: (None, "Голосовая модель не загружена"))["status"], "Голосовая модель не загружена")
        self.assertIsNone(session.handle_text("rm -rf /")["intent"])
        with self.assertRaises(ValueError): session.record("/tmp/x", 999, runner=lambda *a, **k: None)
        c = []; session.record("/tmp/x", 3, runner=lambda a, **k: c.append((a, k))); self.assertEqual(c[0][0][0], "arecord"); self.assertFalse(c[0][1]["shell"])
    def test_gui_and_configs(self):
        for f in ("voice_window", "backup"): py_compile.compile(os.path.join(R, "apps", f + ".py"), doraise=True)
        for f in ("etc/lightdm/lightdm-gtk-greeter.conf", "etc/xdg/dunst/dunstrc", "usr/local/bin/nevexona-voice", "usr/local/bin/nevexona-backup"):
            self.assertTrue(os.path.isfile(os.path.join(R, "config/includes.chroot", f)), f)

if __name__ == "__main__":
    unittest.main()
