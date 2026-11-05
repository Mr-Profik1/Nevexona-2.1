#!/usr/bin/env python3
"""Базовые проверки структуры. Не заменяют сборку и запуск на реальном ПК."""
import pathlib, re, subprocess, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Structure(unittest.TestCase):
    def test_dirs(self):
        for d in "config branding desktop apps drivers network laptop gaming security voice ai system installer scripts tests docs .github/workflows".split():
            self.assertTrue((ROOT / d).is_dir(), d)

    def test_files(self):
        for f in "README.md LICENSE .gitignore .env.example CONTINUATION.md".split():
            self.assertTrue((ROOT / f).is_file(), f)

    def test_branding(self):
        for f in "logo.svg logo.png logo.ico favicon.svg favicon.ico boot-logo.svg installer-logo.svg".split():
            p = ROOT / "branding" / f
            self.assertTrue(p.is_file() and p.stat().st_size > 0, f)

    def test_palette_in_logo(self):
        svg = (ROOT / "branding/logo.svg").read_text()
        self.assertIn("#FF781F", svg)
        self.assertIn("#171717", svg)

    def test_package_list(self):
        p = ROOT / "config/package-lists/core.list.chroot"
        names = [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith("#")]
        self.assertTrue(names)
        for n in names:
            self.assertRegex(n, r"^[a-z0-9][a-z0-9+.\-]+$")
        self.assertEqual(len(names), len(set(names)))

    def test_env_example_empty(self):
        for l in (ROOT / ".env.example").read_text().splitlines():
            if "=" in l and not l.startswith("#"):
                self.assertEqual(l.split("=", 1)[1].strip(), "", l)

    def test_no_secrets(self):
        pat = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)")
        for p in ROOT.rglob("*"):
            if p.is_file() and ".git" not in p.parts and p.suffix in {".md",".sh",".yml",".py",".txt",".svg",".list",".chroot"}:
                self.assertIsNone(pat.search(p.read_text(errors="ignore")), str(p))

    def test_scripts_syntax(self):
        for s in (ROOT / "scripts").glob("*.sh"):
            r = subprocess.run(["bash", "-n", str(s)], capture_output=True)
            self.assertEqual(r.returncode, 0, s)

    def test_workflows_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML не установлен")
        for w in (ROOT / ".github/workflows").glob("*.yml"):
            self.assertIsInstance(yaml.safe_load(w.read_text()), dict, w)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Structure))
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if res.wasSuccessful() else 1)
