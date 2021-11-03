from bclearer_source.b_code.common_knowledge.adjustment_operation_types import AdjustmentOperationTypes
from bclearer_source.b_code.configurations.adjustment_operation_configurations import AdjustmentOperationConfigurations
from bclearer_source.b_code.configurations.adjustment_operations_substage_configurations import AdjustmentOperationsSubstageConfigurations
from bclearer_source.b_code.configurations.attribute_to_association_adjustment_operation_configurations import AttributeToAssociationAdjustmentOperationConfigurations
from bclearer_source.b_code.substages.operations.a_load.content_operations.runners.hdf5_to_content_universe_loader import load_hdf5_model_to_content_universe
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.attributes_to_associations_converter import convert_attributes_to_associations
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.remove_attributes.attribute_remover import remove_attributes
from bclearer_source.b_code.substages.operations.b_evolve.common.universes_merge_registers import UniversesMergeRegisters
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers
from nf_ea_common_tools_source.b_code.services.session.processes.creators.empty_nf_ea_com_universe_creator import create_empty_nf_ea_universe


class AdjustmentOperationsSubstages:
    def __init__(
            self,
            ea_tools_session_manager: EaToolsSessionManagers,
            adjustment_operations_substage_configuration: AdjustmentOperationsSubstageConfigurations,
            content_universe: NfEaComUniverses):
        self.ea_tools_session_manager = \
            ea_tools_session_manager

        self.adjustment_operations_substage_configuration = \
            adjustment_operations_substage_configuration

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
        current_content_universe = \
            self.content_universe

        for adjustment_operation_configuration in \
                self.adjustment_operations_substage_configuration.operation_configurations:
            current_output_universe = \
                self.__run_operation(
                    content_universe=current_content_universe,
                    adjustment_operation_configuration=adjustment_operation_configuration)

            current_content_universe = \
                current_output_universe

        return \
            current_content_universe

    def __run_operation(
            self,
            content_universe: NfEaComUniverses,
            adjustment_operation_configuration: AdjustmentOperationConfigurations) \
            -> NfEaComUniverses:
        adjustment_universe = \
            load_hdf5_model_to_content_universe(
                ea_tools_session_manager=self.ea_tools_session_manager,
                load_hdf5_model_configuration=adjustment_operation_configuration.adjustment_universe_load_hdf5_model_configuration)

        universes_merge_register = \
            UniversesMergeRegisters(
                universe_1=content_universe,
                universe_2=adjustment_universe,
                context=self.__class__.__name__)

        output_universe = \
            create_empty_nf_ea_universe(
                ea_tools_session_manager=self.ea_tools_session_manager,
                short_name=adjustment_operation_configuration.output_universe_short_name)

        if adjustment_operation_configuration.operation_type == AdjustmentOperationTypes.REMOVE_ATTRIBUTES:
            remove_attributes(
                content_universe=universes_merge_register.primary_universe,
                adjustment_universe=universes_merge_register.aligned_universe,
                output_universe=output_universe)

        elif adjustment_operation_configuration.operation_type == AdjustmentOperationTypes.CONVERT_ATTRIBUTES_TO_ASSOCIATIONS:
            if not isinstance(adjustment_operation_configuration, AttributeToAssociationAdjustmentOperationConfigurations):
                raise \
                    TypeError(
                        'adjustment_operation_configuration is not AttributeToAssociationAdjustmentOperationConfigurations')

            convert_attributes_to_associations(
                content_universe=universes_merge_register.primary_universe,
                adjustment_universe=universes_merge_register.aligned_universe,
                output_universe=output_universe,
                direction=adjustment_operation_configuration.direction,
                package_name=adjustment_operation_configuration.package_name,
                attribute_to_association_operation_subtype=adjustment_operation_configuration.attribute_to_association_operation_subtype)

        return \
            output_universe
