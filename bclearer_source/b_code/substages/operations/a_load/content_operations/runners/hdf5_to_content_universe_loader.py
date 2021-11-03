import importlib
from pathlib import Path

from nf_common_source.code.services.file_system_service.objects.files import Files
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_common_source.code.services.reporting_service.wrappers.run_and_log_function_wrapper import run_and_log_function
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.general.nf_ea.model_loader.hdf5_loader.hdf5_to_nf_ea_com_universe_loader import \
    load_hdf5_to_nf_ea_com_universe
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import \
    EaToolsSessionManagers

from bclearer_source.b_code.configurations.load_hdf5_model_configurations import LoadHdf5ModelConfigurations
from bclearer_source.b_code.substages.operations.a_load.content_operations.digitalisation_levels.default_digitalisation_level_stereotype_adder import \
    add_default_digitalisation_level_stereotype


@run_and_log_function
def load_hdf5_model_to_content_universe(
        ea_tools_session_manager: EaToolsSessionManagers,
        load_hdf5_model_configuration: LoadHdf5ModelConfigurations) \
        -> NfEaComUniverses:
    log_message(
        message='CONTENT OPERATION: Load universe from HDF5 - ' +
                load_hdf5_model_configuration.universe_short_name + ' - started')

    hdf5_file = \
        __get_hdf5_file(
            resource_namespace=load_hdf5_model_configuration.resource_namespace,
            resource_file_name=load_hdf5_model_configuration.resource_file_name)

    output_universe = \
        load_hdf5_to_nf_ea_com_universe(
            ea_tools_session_manager=ea_tools_session_manager,
            hdf5_file=hdf5_file,
            short_name=load_hdf5_model_configuration.universe_short_name)

    if load_hdf5_model_configuration.default_digitalisation_level_stereotype:
        add_default_digitalisation_level_stereotype(
            nf_ea_com_universe=output_universe,
            default_digitalisation_level_stereotype=load_hdf5_model_configuration.default_digitalisation_level_stereotype)

    log_message(
        message='CONTENT OPERATION: Load universe from HDF5 - ' +
                load_hdf5_model_configuration.universe_short_name + ' - finished')

    return \
        output_universe


def __get_empty_nf_ea_com_universe(
        ea_tools_session_manager: EaToolsSessionManagers,
        short_name: str) \
        -> NfEaComUniverses:
    ea_repository = \
        ea_tools_session_manager.create_empty_ea_repository_with_short_name(
            short_name=short_name)

    nf_ea_com_universe_manager = \
        ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager

    nf_ea_com_universe = \
        nf_ea_com_universe_manager.nf_ea_com_universe_dictionary[ea_repository]

    return \
        nf_ea_com_universe


def __get_hdf5_file(
        resource_namespace: str,
        resource_file_name: str) \
        -> Files:
    resource_namespace_module = \
        importlib.import_module(
            name=resource_namespace)

    resource_namespace_folder_name = \
        resource_namespace_module.__path__[0]

    resource_folder_path = \
        Path(
            resource_namespace_folder_name)

    hdf5_file_name = \
        resource_folder_path.joinpath(
            resource_file_name)

    hdf5_file = \
        Files(
            absolute_path_string=str(hdf5_file_name))

    return \
        hdf5_file
