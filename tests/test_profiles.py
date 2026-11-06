import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from system import profiles

class P(unittest.TestCase):
    def test_recommend(self):
        G = 2**30
        self.assertEqual(profiles.recommend(1 * G), "ULTRA LOW")
        self.assertEqual(profiles.recommend(2 * G), "LOW")
        self.assertEqual(profiles.recommend(4 * G), "NORMAL")
        self.assertEqual(profiles.recommend(8 * G), "PERFORMANCE")
        self.assertEqual(profiles.recommend(16 * G), "GAMING")
    def test_never_disables_security_or_network(self):
        for n, p in profiles.PROFILES.items():
            for a in p["autostart_off"]:
                self.assertNotIn(a.lower(), profiles.FORBIDDEN, n)
    def test_save(self):
        with tempfile.TemporaryDirectory() as t:
            profiles.save("LOW", os.path.join(t, "x", "p.json"))
            with self.assertRaises(ValueError):
                profiles.save("TURBO", os.path.join(t, "p.json"))
    def test_configs_exist(self):
        r = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for f in ["config/includes.chroot/etc/sysctl.d/99-nevexona.conf", "config/includes.chroot/etc/default/zramswap",
                  "config/hooks/live/0100-lowram.hook.chroot"]:
            self.assertTrue(os.path.isfile(os.path.join(r, f)), f)

if __name__ == "__main__":
    unittest.main()
