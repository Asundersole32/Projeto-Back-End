from machines.machines_data_models.automated_optical_inspection import AutomatedOpticalInspection
from machines.machines_data_models.automated_stencil_printer import AutomatedStencilPrinter
from machines.machines_data_models.pick_and_place import PickAndPlace
from machines.machines_data_models.reflow_oven import ReflowOven
from machines.machines_data_models.solder_paste_inspection import SolderPasteInspection

from machines.models import MachineData


class SeededDataGenerator():
    def __init__(self, aoi_id, automated_stencil_printer_id, pick_and_place_id, reflow_oven_id, spi_id):
        self.aoi = AutomatedOpticalInspection(aoi_id)
        self.automated_stencil_printer = AutomatedStencilPrinter(automated_stencil_printer_id)
        self.pick_and_place = PickAndPlace(pick_and_place_id)
        self.reflow_oven = ReflowOven(reflow_oven_id)
        self.spi = SolderPasteInspection(spi_id)

    def execute(self):
        aoi_data = self.aoi.generate_data()
        automated_stencil_printer_data = self.automated_stencil_printer.generate_data()
        pick_and_place_data = self.pick_and_place.generate_data()
        reflow_oven_data = self.reflow_oven.generate_data()
        spi_data = self.spi.generate_data()

        MachineData.objects.create(
            machine = self.aoi.machine_id,
            data = aoi_data
        )

        MachineData.objects.create(
            machine = self.automated_stencil_printer.machine_id,
            data = automated_stencil_printer_data
        )

        MachineData.objects.create(
            machine = self.pick_and_place.machine_id,
            data = pick_and_place_data
        )

        MachineData.objects.create(
            machine = self.reflow_oven.machine_id,
            data = reflow_oven_data
        )

        MachineData.objects.create(
            machine = self.spi.machine_id,
            data = spi_data
        )



