import csv
import os
from nf_common_source.code.services.input_output_service.delimited_text.dataframe_dictionary_to_csv_files_writer import write_dataframe_dictionary_to_csv_files
from nf_ea_common_tools_source.b_code.services.general.nf_ea.domain_migration.nf_ea_com_to_domain_migration.processes.nf_ea_com_to_standard_tables_dictionary_converter import convert_nf_ea_com_to_standard_tables_dictionary
from bclearer_source.b_code.configurations.run_configurations import RunConfigurations
from nf_common_source.code.services.file_system_service.objects.files import Files
from nf_common_source.code.services.log_environment_utility_service.common_knowledge.constants import NAME_VALUE_DELIMITER
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_common_source.code.services.reporting_service.wrappers.run_and_log_function_wrapper import run_and_log_function
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


@run_and_log_function
def instrument_and_visualize(
        output_folder_name: str,
        visualization_substage_output_universe: NfEaComUniverses):
    __report_summary(
        visualization_substage_output_universe=visualization_substage_output_universe,
        output_folder_name=output_folder_name)

    if RunConfigurations.hdf5_output:
        __write_hdf5_file(
            output_folder_name=output_folder_name,
            visualization_substage_output_universe=visualization_substage_output_universe)

    if RunConfigurations.csv_output:
        __export_to_csv(
            output_folder_name=output_folder_name,
            visualization_substage_output_universe=visualization_substage_output_universe)


def __report_summary(
        visualization_substage_output_universe: NfEaComUniverses,
        output_folder_name: str) \
        -> None:
    visualization_substage_output_universe.nf_ea_com_registry.create_or_update_nf_ea_com_summary_table()

    visualization_substage_identifier_code = \
        visualization_substage_output_universe.ea_repository.short_name

    summary_table_by_type = \
        visualization_substage_output_universe.nf_ea_com_registry.dictionary_of_collections[
            NfEaComCollectionTypes.SUMMARY_TABLE_BY_TYPE]

    summary_table_by_type_filtered = \
        summary_table_by_type.loc[
            (summary_table_by_type['minor_types'] == EaConnectorTypes.ASSOCIATION.type_name) |
            (summary_table_by_type['minor_types'] == 'Attribute') |
            (summary_table_by_type['minor_types'] == EaConnectorTypes.DEPENDENCY.type_name) |
            (summary_table_by_type['minor_types'] == EaConnectorTypes.GENERALIZATION.type_name) |
            (summary_table_by_type['minor_types'] == EaElementTypes.CLASS.type_name) |
            (summary_table_by_type['minor_types'] == EaElementTypes.OBJECT.type_name) |
            (summary_table_by_type['minor_types'] == 'Stereotype_usage')]

    visualization_substage_folder_path = \
        os.path.join(
            output_folder_name,
            visualization_substage_output_universe.ea_repository.short_name)

    os.mkdir(
        visualization_substage_folder_path)

    summary_file_full_path = \
        os.path.join(
            visualization_substage_folder_path,
            visualization_substage_output_universe.ea_repository.short_name + '_summary.csv')

    summary_table_by_type_filtered.to_csv(
        path_or_buf=summary_file_full_path,
        sep=',',
        quotechar='"',
        index=False,
        quoting=csv.QUOTE_ALL)

    for summary_tuple in summary_table_by_type_filtered.itertuples():
        main_type = \
            get_tuple_attribute_value_if_required(
                owning_tuple=summary_tuple,
                attribute_name='main_types')
        minor_type = \
            get_tuple_attribute_value_if_required(
                owning_tuple=summary_tuple,
                attribute_name='minor_types')
        row_count = \
            get_tuple_attribute_value_if_required(
                owning_tuple=summary_tuple,
                attribute_name='row_count')

        message_list = \
            [
                '@count@',
                visualization_substage_identifier_code,
                main_type,
                minor_type,
                str(row_count)
            ]

        log_message(
            message=NAME_VALUE_DELIMITER.join(message_list))


def __report_dependency_depth(
        visualization_substage_output_universe: NfEaComUniverses) \
        -> None:
    visualization_substage_output_universe.nf_ea_com_registry.create_or_update_dependency_depths_table()

    dependency_depths_table = \
        visualization_substage_output_universe.nf_ea_com_registry.dictionary_of_collections[
            NfEaComCollectionTypes.DEPENDENCY_DEPTHS_TABLE]

    log_message(
        message='The type-instance depth of this model is: ' + str(dependency_depths_table['level_depth'].max()))

    print(
        dependency_depths_table)


def __write_hdf5_file(
        output_folder_name: str,
        visualization_substage_output_universe: NfEaComUniverses) \
        -> None:
    visualization_substage_identifier_code = \
        visualization_substage_output_universe.ea_repository.short_name

    hdf5_directory_path = \
        os.path.join(
            output_folder_name,
            visualization_substage_identifier_code)

    hdf5_file_name = \
        visualization_substage_identifier_code + '_hdf5_export.hdf5'

    hdf5_file_path = \
        os.path.join(
            hdf5_directory_path,
            hdf5_file_name)

    hdf5_file = \
        Files(
            absolute_path_string=str(hdf5_file_path))

    visualization_substage_output_universe.nf_ea_com_registry.export_registry_to_hdf5(
        hdf5_file=hdf5_file)


def __export_to_csv(
        output_folder_name: str,
        visualization_substage_output_universe: NfEaComUniverses) \
        -> None:
    universe_as_standard_tables_dictionary = \
        convert_nf_ea_com_to_standard_tables_dictionary(
            nf_ea_com_universe=visualization_substage_output_universe)

    visualization_substage_identifier_code = \
        visualization_substage_output_universe.ea_repository.short_name

    csv_directory_path = \
        os.path.join(
            output_folder_name,
            visualization_substage_identifier_code,
            'csv')

    os.mkdir(
        csv_directory_path)

    write_dataframe_dictionary_to_csv_files(
        folder_name=csv_directory_path,
        dataframes_dictionary=universe_as_standard_tables_dictionary)
