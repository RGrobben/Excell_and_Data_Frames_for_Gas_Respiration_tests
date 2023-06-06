import dataclasses
from dataclasses import dataclass

@dataclass()
class Constants_Sample:
    Rgas: float
    expTemp: float
    volume_headspace: float
    water_volume: float
    dry_mass_sample: float
    molar_mass_carbon: float = 12
    henryeff_20: float = 5.23**-3
