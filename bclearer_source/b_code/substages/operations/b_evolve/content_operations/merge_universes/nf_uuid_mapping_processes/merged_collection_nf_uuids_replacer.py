from pandas import DataFrame
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_uuid_mapping_processes.uuid_columns_lists_constants import LIST_OF_NF_UUID_COLUMN_NAMES
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_uuid_mapping_processes.uuid_columns_lists_constants import LIST_OF_NF_UUID_LISTS_COLUMN_NAMES


def replace_nf_uuids_in_collection(
        column_name: str,
        nf_uuid_mapping_dictionary: dict,
        collection: DataFrame) \
        -> DataFrame:
    column_has_lists = \
        __check_column_has_lists(
            column_name=column_name,
            dataframe=collection)

    if column_has_lists:
        if column_name in LIST_OF_NF_UUID_LISTS_COLUMN_NAMES:
            collection_with_nf_uuids_replaced = \
                __update_nf_uuids_list_column_in_dataframe(
                    nf_uuid_mapping_dictionary=nf_uuid_mapping_dictionary,
                    dataframe=collection,
                    uuid_list_column_name=column_name)

        else:
            collection_with_nf_uuids_replaced = \
                collection

    else:
        if column_name in LIST_OF_NF_UUID_COLUMN_NAMES:
            collection_with_nf_uuids_replaced = \
                __update_nf_uuids_column_in_dataframe(
                    nf_uuid_mapping_dictionary=nf_uuid_mapping_dictionary,
                    dataframe=collection,
                    uuid_column_name=column_name)

        else:
            collection_with_nf_uuids_replaced = \
                collection

    return \
        collection_with_nf_uuids_replaced


def __check_column_has_lists(
        column_name: str,
        dataframe: DataFrame) \
        -> bool:
    dataframe_of_types = \
        dataframe.applymap(
            type)

    dataframe_of_lists = \
        dataframe_of_types.loc[dataframe_of_types[column_name].astype(str) == "<class 'list'>"]

    column_has_lists = \
        dataframe_of_lists.shape[0] > 0

    return \
        column_has_lists


def __update_nf_uuids_column_in_dataframe(
        nf_uuid_mapping_dictionary: dict,
        dataframe: DataFrame,
        uuid_column_name: str) \
        -> DataFrame:
    updated_dataframe = \
        dataframe.copy()

    updated_dataframe[uuid_column_name] = \
        updated_dataframe[uuid_column_name].apply(
            lambda original_nf_uuid: __replace_original_nf_uuid_by_new_nf_uuid(
                original_nf_uuid=original_nf_uuid,
                nf_uuid_mapping_dictionary=nf_uuid_mapping_dictionary))

    return \
        updated_dataframe


def __update_nf_uuids_list_column_in_dataframe(
        nf_uuid_mapping_dictionary: dict,
        dataframe: DataFrame,
        uuid_list_column_name: str) \
        -> DataFrame:
    updated_dataframe = \
        dataframe.copy()

    updated_dataframe[uuid_list_column_name] = \
        dataframe[uuid_list_column_name].apply(
            lambda list_of_uuids: __replace_list_of_uuids(
                list_of_uuids=list_of_uuids,
                nf_uuid_mapping_dictionary=nf_uuid_mapping_dictionary))

    return \
        updated_dataframe


def __replace_list_of_uuids(
        list_of_uuids: list,
        nf_uuid_mapping_dictionary: dict) \
        -> list:
    list_of_new_uuids = \
        []

    if not isinstance(list_of_uuids, list):
        return \
            list_of_new_uuids

    for original_uuid in list_of_uuids:
        list_of_new_uuids.append(
            __replace_original_nf_uuid_by_new_nf_uuid(
                original_nf_uuid=original_uuid,
                nf_uuid_mapping_dictionary=nf_uuid_mapping_dictionary))

    return \
        list_of_new_uuids


def __replace_original_nf_uuid_by_new_nf_uuid(
        original_nf_uuid: str,
        nf_uuid_mapping_dictionary: dict) \
        -> str:
    try:
        new_nf_uuid = \
            nf_uuid_mapping_dictionary[original_nf_uuid]

    except KeyError:
        new_nf_uuid = \
            original_nf_uuid

    return \
        new_nf_uuid

