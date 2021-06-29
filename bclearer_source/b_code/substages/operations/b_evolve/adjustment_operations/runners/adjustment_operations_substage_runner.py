from bclearer_source.b_code.configurations.adjustment_operations_substage_configurations import AdjustmentOperationsSubstageConfigurations
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.adjustment_operations_substages import AdjustmentOperationsSubstages
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers


def run_adjustment_operations_substage(
        ea_tools_session_manager: EaToolsSessionManagers,
        content_universe: NfEaComUniverses,
        adjustment_operations_substage_configuration: AdjustmentOperationsSubstageConfigurations) \
        -> NfEaComUniverses:
    with AdjustmentOperationsSubstages(
            ea_tools_session_manager=ea_tools_session_manager,
            content_universe=content_universe,
            adjustment_operations_substage_configuration=adjustment_operations_substage_configuration) \
            as adjustment_operations_substage:
        adjustment_operations_substage_output_universe = \
            adjustment_operations_substage.run()

        return \
            adjustment_operations_substage_output_universe
