from dataclasses import dataclass

from validation_input_data.general_validation_functions import validate_if_there_is_a_float_or_integer_in_cell


@dataclass
class ConstantsSample:
    Rgas: float = None
    expTemp: float = None
    volume_headspace: float = None
    water_volume: float = None
    dry_mass_sample: float = None
    molar_mass_carbon: float = 12
    henryeff_20: float = 5.23 ** -3

    def check_all_checks(self):
        checks = [
            self.check_Rgas,
            self.check_expTemp,
            self.check_volume_headspace,
            self.check_water_volume,
            self.check_dry_mass_sample,
            self.check_molar_mass_carbon,
        ]
        error_messages = []

        for check in checks:
            if check is not True:
                error_messages.append(check)

        if not error_messages:
            return True
        else:
            return error_messages

    @property
    def check_Rgas(self):
        check_if_float = isinstance(self.Rgas, float)
        if not check_if_float:
            return "Rgas is not a float"
        return True

    @property
    def check_expTemp(self):
        check_if_float = isinstance(self.expTemp, float)
        if not check_if_float:
            return "expTemp is not a float"
        return True

    @property
    def check_volume_headspace(self):
        check_if_float = isinstance(self.volume_headspace, float)
        if not check_if_float:
            return "volume_headspace is not a float"
        return True

    @property
    def check_water_volume(self):
        check_if_float = isinstance(self.water_volume, float)
        if not check_if_float:
            return "water_volume is not a float"
        return True

    @property
    def check_dry_mass_sample(self):
        check_if_float = isinstance(self.dry_mass_sample, float)
        if not check_if_float:
            return "dry_mass_sample is not a float"
        return True

    @property
    def check_molar_mass_carbon(self):
        check_if_float = isinstance(self.molar_mass_carbon, float)
        check_if_float_is_oke = False
        if self.molar_mass_carbon == 12 or self.molar_mass_carbon == 12.011:
            check_if_float_is_oke = True

        if not check_if_float or check_if_float_is_oke:
            return "molar_mass_carbon is not correct"
        return True


@dataclass
class FillType:
    solid = "solid"
    gradient = "gradient"
    pattern = "pattern"
    none = "none"


@dataclass
class OwnColors:
    # RGB codes of colors
    red = "FFFF0000"
    blue = "FF0000FF"
    green = "FF00FF00"
    yellow = "FFFFFF00"
