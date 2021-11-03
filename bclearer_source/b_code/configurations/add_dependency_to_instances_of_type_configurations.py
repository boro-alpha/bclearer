from bclearer_source.b_code.common_knowledge.universe_modification_operation_types import \
    UniverseModificationOperationTypes
from bclearer_source.b_code.configurations.add_dependency_to_instances_of_type_configuration_objects import \
    AddDependencyToInstancesOfTypeConfigurationObjects
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations


class AddDependencyToInstancesOfTypeConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            add_dependency_to_instances_of_type_operation_type: UniverseModificationOperationTypes,
            configuration_object: AddDependencyToInstancesOfTypeConfigurationObjects,
            output_universe_short_name: str):
        super().__init__(
            operation_type=add_dependency_to_instances_of_type_operation_type)

        self.configuration_object = \
            configuration_object

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
