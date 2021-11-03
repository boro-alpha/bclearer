from bclearer_source.b_code.common_knowledge.universe_modification_operation_types import \
    UniverseModificationOperationTypes
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations
from bclearer_source.b_code.configurations.universe_modification_configuration_objects import \
    UniverseModificationConfigurationObjects


class UniverseModificationOperationConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            universe_modification_operation_type: UniverseModificationOperationTypes,
            output_universe_short_name: str,
            universe_modification_configuration_object: UniverseModificationConfigurationObjects = None,
            package_name: str = None):
        super().__init__(
            operation_type=universe_modification_operation_type)

        self.output_universe_short_name = \
            output_universe_short_name

        self.universe_modification_configuration_object = \
            universe_modification_configuration_object

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
