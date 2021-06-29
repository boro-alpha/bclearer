from bclearer_source.b_code.common_knowledge.adjustment_operation_types import AdjustmentOperationTypes
from bclearer_source.b_code.configurations.load_hdf5_model_configurations import LoadHdf5ModelConfigurations
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations


class AdjustmentOperationConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            adjustment_operation_type: AdjustmentOperationTypes,
            adjustment_universe_load_hdf5_model_configuration: LoadHdf5ModelConfigurations,
            output_universe_short_name: str):
        super().__init__(
            operation_type=adjustment_operation_type)

        self.adjustment_universe_load_hdf5_model_configuration = \
            adjustment_universe_load_hdf5_model_configuration

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
