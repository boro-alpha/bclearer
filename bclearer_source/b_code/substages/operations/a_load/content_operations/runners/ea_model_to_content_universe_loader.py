from bclearer_source.b_code.configurations.load_ea_model_configurations import LoadEaModelConfigurations
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_common_source.code.services.reporting_service.wrappers.run_and_log_function_wrapper import run_and_log_function
from nf_common_source.code.services.resources_service.processes.resource_file_getter import get_resource_file
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers
from nf_ea_common_tools_source.b_code.services.session.processes.creators.new_nf_ea_com_universe_using_file_creator import create_new_nf_ea_com_universe_using_file


@run_and_log_function
def load_ea_model_to_content_universe(
        ea_tools_session_manager: EaToolsSessionManagers,
        load_ea_model_configuration: LoadEaModelConfigurations) \
        -> NfEaComUniverses:
    log_message(
        message='CONTENT OPERATION: Load universe - ' +
                load_ea_model_configuration.short_name + ' - started')

    ea_repository_file = \
        get_resource_file(
            resource_namespace=load_ea_model_configuration.resource_namespace,
            resource_name=load_ea_model_configuration.resource_name)

    output_universe = \
        create_new_nf_ea_com_universe_using_file(
            ea_tools_session_manager=ea_tools_session_manager,
            ea_repository_file=ea_repository_file,
            short_name=load_ea_model_configuration.short_name)

    log_message(
        message='CONTENT OPERATION: Load universe - ' +
                load_ea_model_configuration.short_name + ' - finished')

    return \
        output_universe
