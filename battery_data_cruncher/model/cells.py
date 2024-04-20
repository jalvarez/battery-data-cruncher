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
