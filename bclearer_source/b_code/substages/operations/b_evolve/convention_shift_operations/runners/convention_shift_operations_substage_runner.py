from bclearer_source.b_code.configurations.convention_shift_operation_configurations import ConventionShiftOperationConfigurations
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shift_operations_substages import ConventionShiftOperationsSubstages
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers


def run_convention_shift_operation_substage(
        ea_tools_session_manager: EaToolsSessionManagers,
        content_universe: NfEaComUniverses,
        convention_shift_operation_configuration: ConventionShiftOperationConfigurations) \
        -> NfEaComUniverses:
    with ConventionShiftOperationsSubstages(
            ea_tools_session_manager=ea_tools_session_manager,
            convention_shift_operation_configuration=convention_shift_operation_configuration,
            content_universe=content_universe) \
            as convention_shift_operations_substage:
        convention_shift_operations_substage_output_universe = \
            convention_shift_operations_substage.run()

        return \
            convention_shift_operations_substage_output_universe
