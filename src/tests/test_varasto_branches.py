import unittest
from varasto import Varasto


class TestVarastoBranches(unittest.TestCase):
    def test_tilavuus_nollataan_jos_negatiivinen(self):
        v = Varasto(-1)
        self.assertAlmostEqual(v.tilavuus, 0.0)

    def test_alkusaldo_negatiivinen_nollataan(self):
        v = Varasto(10, -5)
        self.assertAlmostEqual(v.saldo, 0.0)

    def test_alkusaldo_suurempi_kuin_tilavuus_tayteen(self):
        v = Varasto(5, 10)
        self.assertAlmostEqual(v.saldo, 5)

    def test_lisaa_negatiivinen_ei_vaikuta(self):
        v = Varasto(10, 2)
        v.lisaa_varastoon(-3)
        self.assertAlmostEqual(v.saldo, 2)

    def test_lisaa_yli_tilavuuden_tayteen(self):
        v = Varasto(10, 2)
        v.lisaa_varastoon(20)
        self.assertAlmostEqual(v.saldo, 10)

    def test_ota_negatiivinen_palauttaa_nolla(self):
        v = Varasto(10, 4)
        saatu = v.ota_varastosta(-2)
        self.assertAlmostEqual(saatu, 0.0)
        self.assertAlmostEqual(v.saldo, 4)

    def test_ota_enemman_kuin_saldo_palauttaa_kaiken(self):
        v = Varasto(10, 3)
        saatu = v.ota_varastosta(5)
        self.assertAlmostEqual(saatu, 3)
        self.assertAlmostEqual(v.saldo, 0.0)

    def test_str_palauttaa_odotetun(self):
        v = Varasto(10, 5)
        self.assertEqual(
            str(v), f"saldo = {v.saldo}, vielä tilaa {v.paljonko_mahtuu()}")


if __name__ == '__main__':
    unittest.main()
