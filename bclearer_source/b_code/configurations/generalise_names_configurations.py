from bclearer_source.b_code.common_knowledge.convention_shift_operation_types import ConventionShiftOperationTypes
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations


class GeneraliseNamesConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            convention_shift_operation_type: ConventionShiftOperationTypes,
            list_of_configuration_objects: list,
            output_universe_short_name: str):
        super().__init__(
            operation_type=convention_shift_operation_type)

        self.list_of_configuration_objects = \
            list_of_configuration_objects

        self.output_universe_short_name = \
            output_universe_short_name

    def __enter__(
            self):
        return \
            self

    def __exit__(
            self,
            exception_type,
            exception_value,
            traceback):
        pass
