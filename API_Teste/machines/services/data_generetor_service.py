from machines.machines_data_models.automated_optical_inspection import AutomatedOpticalInspection
from machines.machines_data_models.automated_stencil_printer import AutomatedStencilPrinter
from machines.machines_data_models.pick_and_place import PickAndPlace
from machines.machines_data_models.reflow_oven import ReflowOven
from machines.machines_data_models.solder_paste_inspection import SolderPasteInspection

from machines.models import MachineData, Machine


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

        aoi = Machine.objects.get(pk=self.aoi.machine_id)
        automated_stencil_printer = Machine.objects.get(pk=self.automated_stencil_printer.machine_id)
        pick_and_place = Machine.objects.get(pk=self.pick_and_place.machine_id)
        reflow_oven = Machine.objects.get(pk=self.reflow_oven.machine_id)
        spi = Machine.objects.get(pk=self.spi.machine_id)

        MachineData.objects.create(
            machine = aoi,
            data = aoi_data
        )

        MachineData.objects.create(
            machine = automated_stencil_printer,
            data = automated_stencil_printer_data
        )

        MachineData.objects.create(
            machine = pick_and_place,
            data = pick_and_place_data
        )

        MachineData.objects.create(
            machine = reflow_oven,
            data = reflow_oven_data
        )

        MachineData.objects.create(
            machine = spi,
            data = spi_data
        )



