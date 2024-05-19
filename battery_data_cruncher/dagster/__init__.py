from dataclasses import fields, astuple
from dagster import (
    repository,
    op,
    job,
    DynamicOut,
    DynamicOutput,
    InMemoryIOManager,
    In,
    in_process_executor,
)

from ..model import BatteryCell, BatteryCellData
from ..sources.secondlife import cell_index_iterator, extract_cell_details


@op(ins={"cell_data": In(BatteryCellData)})
def get_battery_cell_data(context, cell_data: BatteryCellData):
    context.log.debug(f"Processing {cell_data.brand}-{cell_data.model}")
    details = extract_cell_details(cell_data.cell_data_url)
    return BatteryCell.from_data(cell_data, *details)


@op(out=DynamicOut(BatteryCellData))
def get_second_life_index():
    """Get index from the secondlife source"""
    for idx, cell_data in enumerate(cell_index_iterator()):
        partial_cell = BatteryCellData(*cell_data)
        yield DynamicOutput(partial_cell, mapping_key=f"cell_{idx}")


@op
def write_models(context, models_data):
    if len(models_data) > 0:
        csv_fields = list(map(lambda _: _.name, fields(models_data[0])))
        with open("output/models.csv", "wt") as output_file:
            output_file.write(",".join(csv_fields))
            output_file.write("\n")
            for model in models_data:
                output_file.write(",".join(map(str, astuple(model))))
                output_file.write("\n")
    context.log.info(f"Battery cell models processed: {len(models_data)}")


@job(
    executor_def=in_process_executor, resource_defs={"io_manager": InMemoryIOManager()}
)
def get_secondlife_data():
    """Get data from secondlife source"""
    cell_index = get_second_life_index()
    models_data = cell_index.map(get_battery_cell_data).collect()
    write_models(models_data)


@repository
def battery_data_repo():
    return [get_secondlife_data]
