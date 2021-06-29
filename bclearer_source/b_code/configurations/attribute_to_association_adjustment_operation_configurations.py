from bclearer_source.b_code.common_knowledge.adjustment_operation_types import AdjustmentOperationTypes
from bclearer_source.b_code.configurations.adjustment_operation_configurations import AdjustmentOperationConfigurations
from bclearer_source.b_code.configurations.load_hdf5_model_configurations import LoadHdf5ModelConfigurations
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import EaAssociationDirectionTypes


class AttributeToAssociationAdjustmentOperationConfigurations(
        AdjustmentOperationConfigurations):
    def __init__(
            self,
            adjustment_operation_type: AdjustmentOperationTypes,
            adjustment_universe_load_hdf5_model_configuration: LoadHdf5ModelConfigurations,
            output_universe_short_name: str,
            direction: EaAssociationDirectionTypes,
            package_name: str):
        super().__init__(
            adjustment_operation_type=adjustment_operation_type,
            adjustment_universe_load_hdf5_model_configuration=adjustment_universe_load_hdf5_model_configuration,
            output_universe_short_name=output_universe_short_name)

        self.direction = \
            direction

        self.package_name = \
            package_name

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
