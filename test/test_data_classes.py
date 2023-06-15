import unittest

from data_classes import ConstantsSample


class ConstantsSampleTestCase(unittest.TestCase):

    def setUp(self):
        self.constants = ConstantsSample(
            Rgas=8.314,
            expTemp=300.0,
            volume_headspace=0.5,
            water_volume=10.0,
            dry_mass_sample=5.0
        )

    def test_check_all_checks(self):
        self.assertTrue(self.constants.check_all_checks)

    def test_check_Rgas(self):
        self.assertTrue(self.constants.check_Rgas)

    def test_check_expTemp(self):
        self.assertTrue(self.constants.check_expTemp)

    def test_check_volume_headspace(self):
        self.assertTrue(self.constants.check_volume_headspace)

    def test_check_water_volume(self):
        self.assertTrue(self.constants.check_water_volume)

    def test_check_dry_mass_sample(self):
        self.assertTrue(self.constants.check_dry_mass_sample)

    def test_check_all_checks_incorrect(self):
        constants = self.constants
        constants.Rgas = "invalid"
        constants.expTemp = [1, 2, 3]
        constants.volume_headspace = "invalid"
        constants.water_volume = None
        constants.dry_mass_sample = True

        all_checks = constants.check_all_checks
        self.assertIsInstance(all_checks, list)
        self.assertIsInstance(all_checks[0], str)
        print(all_checks)

    def test_check_Rgas_incorrect(self):
        # Invalid value: Rgas is a string instead of a float
        constants = self.constants
        constants.Rgas = "invalid"
        self.assertEqual(constants.check_Rgas, "Rgas is not a float")

    def test_check_expTemp_incorrect(self):
        # Invalid value: expTemp is a list instead of a float
        constants = self.constants
        constants.expTemp = [1, 2, 3]
        self.assertEqual(constants.check_expTemp, "expTemp is not a float")

    def test_check_volume_headspace_incorrect(self):
        # Invalid value: volume_headspace is a string instead of a float
        constants = self.constants
        constants.volume_headspace = "invalid"
        self.assertEqual(constants.check_volume_headspace, "volume_headspace is not a float")

    def test_check_water_volume_incorrect(self):
        # Invalid value: water_volume is None instead of a float
        constants = self.constants
        constants.water_volume = None
        self.assertEqual(constants.check_water_volume, "water_volume is not a float")

    def test_check_dry_mass_sample_incorrect(self):
        # Invalid value: dry_mass_sample is a boolean instead of a float
        constants = self.constants
        constants.dry_mass_sample = True
        self.assertEqual(constants.check_dry_mass_sample, "dry_mass_sample is not a float")


if __name__ == '__main__':
    unittest.main()
