from dataclasses import dataclass

from validation_input_data.general_validation_functions import validate_if_there_is_a_float_or_integer_in_cell


@dataclass
class ConstantsSample:
    Rgas: float
    expTemp: float
    volume_headspace: float
    water_volume: float
    dry_mass_sample: float
    molar_mass_carbon: float = 12
    henryeff_20: float = 5.23 ** -3

    @property
    def check_all_constants_filled(self):
        pass

    @property
    def check_Rgas(self):
        check_if_float = isinstance(self.Rgas, float)
        return check_if_float

    @property
    def check_expTemp(self):
        check_if_float = isinstance(self.expTemp, float)
        return check_if_float

    @property
    def check_volume_headspace(self):
        check_if_float = isinstance(self.volume_headspace, float)
        return check_if_float

    @property
    def check_water_volume(self):
        check_if_float = isinstance(self.water_volume, float)
        return check_if_float

    @property
    def check_dry_mass_sample(self):
        check_if_float = isinstance(self.dry_mass_sample, float)
        return check_if_float

    @property
    def check_molar_mass_carbon(self):
        check_if_float = isinstance(self.molar_mass_carbon, float)
        check_if_float_is_oke = False
        if self.molar_mass_carbon == 12 or 12.011:
            check_if_float_is_oke = True

        if check_if_float and check_if_float_is_oke:
            return True

    @property
    def check_henryeff_20(self):
        check_if_float = isinstance(self.molar_mass_carbon, float)
        return check_if_float


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
