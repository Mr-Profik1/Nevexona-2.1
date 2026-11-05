import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from drivers.detect import parse_lspci

SAMPLE = """00:02.0 VGA compatible controller [0300]: Intel Corporation HD Graphics [8086:1912]
\tKernel driver in use: i915
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GF119 [GeForce 210] [10de:1040]
\tKernel modules: nouveau
03:00.0 Network controller [0280]: Realtek Semiconductor Co., Ltd. RTL8821CE [10ec:c821]
\tKernel driver in use: rtw_8821ce
04:00.0 Network controller [0280]: Intel Corporation Wireless 8265 [8086:24fd]
"""

class Drivers(unittest.TestCase):
    def test_parse(self):
        d = parse_lspci(SAMPLE)
        self.assertEqual(len(d), 4)
        self.assertEqual(d[0]["driver"], "i915")
        self.assertEqual(d[1]["vendor"], "NVIDIA")
        self.assertEqual(d[1]["status"], "Нет драйвера")
        self.assertIsNone(d[1]["firmware_pkg"])  # не предлагаем проприетарное молча
        self.assertEqual(d[2]["firmware_pkg"], "firmware-realtek")
        self.assertEqual(d[3]["firmware_pkg"], "firmware-iwlwifi")

if __name__ == "__main__":
    unittest.main()
