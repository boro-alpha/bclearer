from bclearer_source.b_code.configurations.content_operation_configurations import ContentOperationConfigurations
from bclearer_source.b_code.configurations.load_hdf5_model_configurations import LoadHdf5ModelConfigurations
from bclearer_source.b_code.substages.operations.a_load.content_operations.runners.hdf5_to_content_universe_loader import load_hdf5_model_to_content_universe
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.content_operations_substages import ContentOperationsSubstages
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers


def run_merge_hdf5_model_content_operations_substage(
        ea_tools_session_manager: EaToolsSessionManagers,
        content_universe_from_input: NfEaComUniverses,
        load_hdf5_model_configuration: LoadHdf5ModelConfigurations,
        content_operation_configuration: ContentOperationConfigurations) \
        -> NfEaComUniverses:
    content_universe_from_hdf5 = \
        load_hdf5_model_to_content_universe(
            ea_tools_session_manager=ea_tools_session_manager,
            load_hdf5_model_configuration=load_hdf5_model_configuration)

    with ContentOperationsSubstages(
            ea_tools_session_manager=ea_tools_session_manager,
            content_1_universe=content_universe_from_input,
            content_2_universe=content_universe_from_hdf5,
            content_operation_configuration=content_operation_configuration) \
            as content_operations_substage:
        content_operations_substage_output_universe = \
            content_operations_substage.run()

        return \
            content_operations_substage_output_universe
