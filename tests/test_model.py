from battery_data_cruncher.model import BatteryCell, BatteryCellData


def test_battery_cell_from_data():
    cell_data = BatteryCellData(
        "brand",
        "model",
        "form_factor",
        "red",
        "blue",
        "http://localhost/image",
        "http://localhost/data",
    )
    other_details = [
        1000,  #     capacity_mah: int
        3.6,  # nominal_voltaje: Decimal
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    cell = BatteryCell.from_data(cell_data, *other_details)

    assert cell.brand == cell_data.brand
    assert cell.model == cell_data.model
