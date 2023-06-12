from dataclasses import dataclass
from enum import Enum


@dataclass()
class Constants_Sample:
    Rgas: float
    expTemp: float
    volume_headspace: float
    water_volume: float
    dry_mass_sample: float
    molar_mass_carbon: float = 12
    henryeff_20: float = 5.23 ** -3


@dataclass(Enum)
class FillType:
    solid = "solid"
    gradient = "gradient"
    pattern = "pattern"
    none = "none"


@dataclass()
class OwnColors(Enum):
    # RGB codes of colors
    red = "FFFF0000"
    blue = "FF0000FF"
    green = "FF00FF00"
    yellow = "FFFFFF00"

