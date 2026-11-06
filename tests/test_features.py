import os, sys, tempfile, types, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from network import center
from laptop import center as lap
from security import scanner
from system import files, display

def fake(out="", rc=0):
    calls = []
    def r(argv, **k):
        calls.append((argv, k)); return types.SimpleNamespace(stdout=out, returncode=rc)
    r.calls = calls; return r

class Net(unittest.TestCase):
    def test_wifi_parse(self):
        n = center.parse_wifi("Home\\:5G:80:WPA2\nHome\\:5G:60:WPA2\nCafe:55:\n:30:WPA2\n")
        self.assertEqual([x["ssid"] for x in n], ["Home:5G", "Cafe"]); self.assertEqual(n[1]["security"], "открытая")
    def test_connect_safe(self):
        f = fake()
        self.assertTrue(center.wifi_connect("Home", "pw", runner=f)["ok"])
        self.assertFalse(f.calls[0][1]["shell"])
        with self.assertRaises(ValueError): center.wifi_connect("--bad", runner=f)
        self.assertNotIn("pw", str(center.wifi_connect("Home", "pw", runner=fake(rc=1))))
    def test_bt(self):
        self.assertEqual(center.parse_bt("Device AA:BB:CC:DD:EE:FF Наушники\nmusor")[0]["name"], "Наушники")
        with self.assertRaises(ValueError): center.bt_action("pair", "x; rm", runner=fake())
        with self.assertRaises(ValueError): center.bt_action("format", runner=fake())
        center.bt_action("connect", "aa:bb:cc:dd:ee:ff", runner=fake())

class Lap(unittest.TestCase):
    def test_battery_brightness(self):
        with tempfile.TemporaryDirectory() as t:
            b = os.path.join(t, "BAT0"); os.makedirs(b)
            for k, v in {"capacity": "87", "status": "Charging", "energy_full": "40", "energy_full_design": "50"}.items(): open(f"{b}/{k}", "w").write(v)
            self.assertEqual(lap.battery(t), {"percent": 87, "status": "Charging", "health_percent": 80})
            self.assertIsNone(lap.battery(os.path.join(t, "none")))
            bl = os.path.join(t, "bl", "x"); os.makedirs(bl); open(bl + "/brightness", "w").write("50"); open(bl + "/max_brightness", "w").write("100")
            w = []; lap.set_brightness(1, os.path.join(t, "bl"), writer=lambda p, v: w.append(v)); self.assertEqual(w, [5])
            with self.assertRaises(FileNotFoundError): lap.set_brightness(50, os.path.join(t, "no"))

class Sec(unittest.TestCase):
    def test_report(self):
        out = "/h/a.txt: Eicar-Test-Signature FOUND\n----------- SCAN SUMMARY -----------\nScanned files: 12\nInfected files: 1\n"
        rep = scanner.scan(["/h"], runner=fake(out))
        self.assertEqual((rep["scanned"], rep["infected"]), (12, 1)); self.assertEqual(rep["detections"][0]["signature"], "Eicar-Test-Signature")
        self.assertIn("не гарантируется", rep["note"])
        with self.assertRaises(ValueError): scanner.scan([])

class Files(unittest.TestCase):
    def test_trash_cycle_and_search(self):
        with tempfile.TemporaryDirectory() as t:
            f = os.path.join(t, "a.txt"); open(f, "w").write("x")
            tr = os.path.join(t, "Trash"); n = files.trash(f, tr)
            self.assertFalse(os.path.exists(f)); self.assertEqual(files.restore(n, tr), f); self.assertTrue(os.path.exists(f))
            self.assertEqual(files.search(t, "*.TXT"), [f])
            os.makedirs(os.path.join(t, "d")); files.copy(f, os.path.join(t, "d")); self.assertTrue(os.path.exists(os.path.join(t, "d", "a.txt")))

class Disp(unittest.TestCase):
    def test_scale(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(display.set_scale(150, t), 144); display.set_scale(200, t)
            self.assertEqual(open(os.path.join(t, ".Xresources")).read().count("Xft.dpi"), 1)
            with self.assertRaises(ValueError): display.set_scale(333, t)

if __name__ == "__main__":
    unittest.main()
