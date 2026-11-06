import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gaming import hub

class Hub(unittest.TestCase):
    def test_steam_scan_and_launch(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "steamapps"))
            open(os.path.join(t, "steamapps", "appmanifest_440.acf"), "w").write('"AppState"\n{\n"appid"\t\t"440"\n"name"\t\t"Team Fortress 2"\n}')
            lib = hub.Library(os.path.join(t, "lib.json"))
            g = lib.find("team", steam_root=t)
            self.assertEqual(len(g), 1)
            calls = []
            hub.launch(g[0], runner=lambda a, **k: calls.append((a, k)))
            self.assertEqual(calls[0][0], ["steam", "steam://rungameid/440"])
            self.assertFalse(calls[0][1]["shell"])
    def test_custom_add_requires_existing_binary(self):
        with tempfile.TemporaryDirectory() as t:
            lib = hub.Library(os.path.join(t, "lib.json"))
            with self.assertRaises(FileNotFoundError):
                lib.add("X", ["/no/such/game"])
            lib.add("Echo", ["echo"])
            self.assertEqual(hub.Library(os.path.join(t, "lib.json")).all(steam_root=t)[0]["name"], "Echo")
    def test_roblox_status_is_honest(self):
        r = [p for p in hub.PLATFORMS if p["id"] == "roblox"][0]
        self.assertIsNone(r["install"])
        self.assertIn("НЕ поддерживается", r["status"]); self.assertIn("Не обещаем", r["status"])

if __name__ == "__main__":
    unittest.main()
