from dataclasses import dataclass


@dataclass
class BatteryCell:
    brand: str
    model: str
    formfactor: str
    wrap_color: str
    ring_color: str
    cell_image_url: str
    cell_data_url: str
