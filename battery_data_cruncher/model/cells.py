from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BatteryCell:
    brand: str
    model: str
    form_factor: str
    wrap_color: str
    ring_color: str
    cell_image_url: str
    cell_data_url: str
    capacity_mah: int
    nominal_voltaje: Decimal
    charging_voltaje: Decimal | None = None
    charging_std_ma: int | None = None
    charging_max_ma: int | None = None
    discharging_cutoff_voltaje: Decimal | None = None
    discharging_std_ma: int | None = None
    discharging_max_ma: int | None = None
    data_ref_url: str | None = None
