from bclearer_source.b_code.common_knowledge.convention_shift_operation_types import ConventionShiftOperationTypes
from bclearer_source.b_code.configurations.convention_shift_operation_configurations import ConventionShiftOperationConfigurations
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.attribute_names_to_name_objects_convention_shifter import shift_convention_attribute_names_to_name_objects
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.digitalisation_levels.universe_to_semantically_grounded_convention_shifter import \
    shift_convention_universe_to_semantically_grounded
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.generalise_names.generalise_names_convention_shifter import shift_convention_generalise_names
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.objects_to_classes_convention_shifter import shift_convention_objects_to_classes
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_instances_and_exemplars.separate_bespoke_instances_and_exemplars_convention_shifter import shift_convention_separate_bespoke_instances_and_exemplars
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_instances_and_exemplars.separate_standard_instances_and_exemplars_convention_shifter import shift_convention_separate_standard_instances_and_exemplars
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.separate_bespoke_names_and_instances_convention_shifter import shift_convention_separate_bespoke_names_and_instances
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.separate_standard_names_and_instances_convention_shifter import shift_convention_separate_standard_names_and_instances
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.uml_names_to_named_objects_convention_shifter import shift_convention_uml_names_to_named_objects
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers
from nf_ea_common_tools_source.b_code.services.session.processes.creators.empty_nf_ea_com_universe_creator import create_empty_nf_ea_universe


class ConventionShiftOperationsSubstages:
    def __init__(
            self,
            ea_tools_session_manager: EaToolsSessionManagers,
            convention_shift_operation_configuration: ConventionShiftOperationConfigurations,
            content_universe: NfEaComUniverses):
        self.ea_tools_session_manager = \
            ea_tools_session_manager

        self.convention_shift_operation_configuration = \
            convention_shift_operation_configuration

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
                short_name=self.convention_shift_operation_configuration.output_universe_short_name)

        if self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.OBJECTS_TO_CLASSES:
            shift_convention_objects_to_classes(
                content_universe=self.content_universe,
                output_universe=output_universe)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.UML_NAME_TO_NAMED_OBJECT:
            shift_convention_uml_names_to_named_objects(
                content_universe=self.content_universe,
                list_of_configuration_objects=self.convention_shift_operation_configuration.list_of_configuration_objects,
                output_universe=output_universe)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.ATTRIBUTE_NAME_TO_NAMED_OBJECT:
            shift_convention_attribute_names_to_name_objects(
                content_universe=self.content_universe,
                list_of_configuration_objects=self.convention_shift_operation_configuration.list_of_configuration_objects,
                output_universe=output_universe)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.GENERALISE_NAMES:
            shift_convention_generalise_names(
                content_universe=self.content_universe,
                list_of_configuration_objects=self.convention_shift_operation_configuration.list_of_configuration_objects,
                output_universe=output_universe)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.SEPARATE_STANDARD_NAMES_AND_INSTANCES:
            shift_convention_separate_standard_names_and_instances(
                content_universe=self.content_universe,
                output_universe=output_universe,
                package_name=self.convention_shift_operation_configuration.package_name)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.SEPARATE_BESPOKE_NAMES_AND_INSTANCES:
            shift_convention_separate_bespoke_names_and_instances(
                content_universe=self.content_universe,
                list_of_configuration_objects=self.convention_shift_operation_configuration.list_of_configuration_objects,
                output_universe=output_universe,
                package_name=self.convention_shift_operation_configuration.package_name)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.SEPARATE_STANDARD_INSTANCES_AND_EXEMPLARS:
            shift_convention_separate_standard_instances_and_exemplars(
                content_universe=self.content_universe,
                output_universe=output_universe,
                package_name=self.convention_shift_operation_configuration.package_name)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.SEPARATE_BESPOKE_INSTANCES_AND_EXEMPLARS:
            shift_convention_separate_bespoke_instances_and_exemplars(
                content_universe=self.content_universe,
                list_of_configuration_objects=self.convention_shift_operation_configuration.list_of_configuration_objects,
                output_universe=output_universe,
                package_name=self.convention_shift_operation_configuration.package_name)

        elif self.convention_shift_operation_configuration.operation_type == ConventionShiftOperationTypes.UNIVERSE_TO_SEMANTICALLY_GROUNDED_DIGITALISATION_LEVEL:
            shift_convention_universe_to_semantically_grounded(
                content_universe=self.content_universe,
                output_universe=output_universe)

        else:
            raise \
                NotImplementedError

        return \
            output_universe
