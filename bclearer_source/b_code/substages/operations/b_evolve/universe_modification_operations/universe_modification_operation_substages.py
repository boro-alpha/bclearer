from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import \
    EaToolsSessionManagers
from nf_ea_common_tools_source.b_code.services.session.processes.creators.empty_nf_ea_com_universe_creator import \
    create_empty_nf_ea_universe

from bclearer_source.b_code.common_knowledge.universe_modification_operation_types import \
    UniverseModificationOperationTypes
from bclearer_source.b_code.configurations.add_dependency_to_instances_of_type_configuration_objects import \
    AddDependencyToInstancesOfTypeConfigurationObjects
from bclearer_source.b_code.configurations.universe_modification_operation_configurations import \
    UniverseModificationOperationConfigurations
from bclearer_source.b_code.substages.operations.b_evolve.universe_modification_operations.universe_modifiers.dependency_to_instances_of_type_adder import \
    add_dependency_to_instances_of_type


class UniverseModificationOperationsSubstages:
    def __init__(
            self,
            ea_tools_session_manager: EaToolsSessionManagers,
            universe_modification_operation_configuration: UniverseModificationOperationConfigurations,
            content_universe: NfEaComUniverses):
        self.ea_tools_session_manager = \
            ea_tools_session_manager

        self.universe_modification_operation_configuration = \
            universe_modification_operation_configuration

        self.content_universe = \
            content_universe

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

    def run(
            self) \
            -> NfEaComUniverses:
        output_universe = \
            create_empty_nf_ea_universe(
                ea_tools_session_manager=self.ea_tools_session_manager,
                short_name=self.universe_modification_operation_configuration.output_universe_short_name)

        universe_modification_configuration_object = \
            self.universe_modification_operation_configuration.universe_modification_configuration_object

        if self.universe_modification_operation_configuration.operation_type == UniverseModificationOperationTypes.ADD_DEPENDENCY_TO_INSTANCES_OF_TYPE:
            if not isinstance(universe_modification_configuration_object,
                              AddDependencyToInstancesOfTypeConfigurationObjects):
                raise \
                    TypeError

            add_dependency_to_instances_of_type(
                content_universe=self.content_universe,
                output_universe=output_universe,
                matched_target_object=universe_modification_configuration_object.matched_target_type,
                matched_source_objects_type=universe_modification_configuration_object.matched_source_objects_type)
        else:
            raise \
                NotImplementedError

        return \
            output_universe
