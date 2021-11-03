from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import EaTXrefColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def remove_attributes(
        content_universe: NfEaComUniverses,
        adjustment_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    __run_input_checks()

    __run_operation(
        content_universe=content_universe,
        adjustment_universe=adjustment_universe,
        output_universe=output_universe)


def __run_operation(
        content_universe: NfEaComUniverses,
        adjustment_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    log_message(
        message='ADJUSTMENT OPERATION: Remove attributes - started')

    content_collections_dictionary = \
        content_universe.nf_ea_com_registry.dictionary_of_collections

    for content_collection_type, content_collection_table in content_collections_dictionary.items():
        __process_content_collection(
            content_collection_type=content_collection_type,
            content_collection_table=content_collection_table,
            adjustment_universe=adjustment_universe,
            output_universe=output_universe)

    # TODO: Report errors

    log_message(
        message='ADJUSTMENT OPERATION: Remove attributes - finished')


def __run_input_checks():
    pass


def __process_content_collection(
        content_collection_type: NfEaComCollectionTypes,
        content_collection_table: DataFrame,
        adjustment_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    output_collections_dictionary = \
        output_universe.nf_ea_com_registry.dictionary_of_collections

    list_of_attribute_ea_guids_to_be_removed = \
        __get_list_of_attribute_ea_guids_to_be_removed(
            adjustment_universe=adjustment_universe)

    if content_collection_type == NfEaComCollectionTypes.EA_ATTRIBUTES:
        output_collections_dictionary[content_collection_type] = \
            __get_filtered_collection(
                list_of_attribute_ea_guids_to_be_removed=list_of_attribute_ea_guids_to_be_removed,
                content_collection_table=content_collection_table,
                ea_guid_column_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name)

    elif content_collection_type == NfEaComCollectionTypes.STEREOTYPE_USAGE:
        output_collections_dictionary[content_collection_type] = \
            __get_filtered_collection(
                list_of_attribute_ea_guids_to_be_removed=list_of_attribute_ea_guids_to_be_removed,
                content_collection_table=content_collection_table,
                ea_guid_column_name=EaTXrefColumnTypes.T_XREF_CLIENT_EA_GUIDS.nf_column_name)

    else:
        output_collections_dictionary[content_collection_type] = \
            content_collection_table


def __get_list_of_attribute_ea_guids_to_be_removed(
        adjustment_universe: NfEaComUniverses) \
        -> list:
    adjustment_collections_dictionary = \
        adjustment_universe.nf_ea_com_registry.dictionary_of_collections

    table_of_attributes_to_be_removed = \
        adjustment_collections_dictionary[NfEaComCollectionTypes.EA_ATTRIBUTES]

    list_of_attribute_ea_guids_to_be_removed = \
        table_of_attributes_to_be_removed[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name].to_list()

    return \
        list_of_attribute_ea_guids_to_be_removed


def __get_filtered_collection(
        list_of_attribute_ea_guids_to_be_removed: list,
        content_collection_table: DataFrame,
        ea_guid_column_name: str) \
        -> DataFrame:
    filtered_collection = \
        content_collection_table[
            ~content_collection_table[ea_guid_column_name].isin(list_of_attribute_ea_guids_to_be_removed)]

    return \
        filtered_collection
