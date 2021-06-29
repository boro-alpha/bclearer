from nf_common_source.code.constants.standard_constants import DEFAULT_FOREIGN_TABLE_SUFFIX
from nf_common_source.code.constants.standard_constants import DEFAULT_MASTER_TABLE_SUFFIX
from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from pandas import DataFrame
from pandas import concat
from pandas import merge

from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def create_aligned_to_primary_universe_nf_uuids_map(
        primary_universe: NfEaComUniverses,
        aligned_universe: NfEaComUniverses) \
        -> dict:
    matched_by_ea_guid_nf_uuids_dataframe = \
        __get_matched_by_ea_guid_mapping_dataframe(
            primary_universe=primary_universe,
            secondary_universe=aligned_universe)

    secondary_to_primary_universe_nf_uuids_map = \
        __get_secondary_to_primary_universe_nf_uuids_map(
            matched_by_ea_guid_nf_uuids_dataframe=matched_by_ea_guid_nf_uuids_dataframe)

    return \
        secondary_to_primary_universe_nf_uuids_map


def __get_matched_by_ea_guid_mapping_dataframe(
        primary_universe: NfEaComUniverses,
        secondary_universe: NfEaComUniverses) \
        -> DataFrame:
    primary_universe_nf_uuids_to_ea_guids_table = \
        __get_universe_nf_uuids_to_ea_guids_table(
            content_universe=primary_universe)

    secondary_universe_nf_uuids_to_ea_guids_table = \
        __get_universe_nf_uuids_to_ea_guids_table(
            content_universe=secondary_universe)

    matched_by_ea_guid_mapping_dataframe = \
        merge(
            left=secondary_universe_nf_uuids_to_ea_guids_table,
            right=primary_universe_nf_uuids_to_ea_guids_table,
            suffixes=(DEFAULT_MASTER_TABLE_SUFFIX, DEFAULT_FOREIGN_TABLE_SUFFIX),
            how='outer',
            on=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name)

    matched_by_ea_guid_mapping_dataframe.drop_duplicates(
        inplace=True)

    return \
        matched_by_ea_guid_mapping_dataframe


def __get_universe_nf_uuids_to_ea_guids_table(
        content_universe: NfEaComUniverses) \
        -> DataFrame:
    universe_nf_uuids_to_ea_guids_table = \
        DataFrame(
            columns=
            [
                NfColumnTypes.NF_UUIDS.column_name,
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
            ])

    for collection_type, collection in content_universe.nf_ea_com_registry.dictionary_of_collections.items():
        universe_nf_uuids_to_ea_guids_table = \
            __add_nf_uuids_to_ea_guids_if_required(
                universe_nf_uuids_to_ea_guids_table=universe_nf_uuids_to_ea_guids_table,
                collection=collection)

    return \
        universe_nf_uuids_to_ea_guids_table


def __add_nf_uuids_to_ea_guids_if_required(
        universe_nf_uuids_to_ea_guids_table: DataFrame,
        collection: DataFrame) \
        -> DataFrame:
    if NfColumnTypes.NF_UUIDS.column_name not in collection.columns:
        return \
            universe_nf_uuids_to_ea_guids_table

    if NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name not in collection.columns:
        return \
            universe_nf_uuids_to_ea_guids_table

    new_mappings = \
        collection.filter(
            items=
            [
                NfColumnTypes.NF_UUIDS.column_name,
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
            ])

    new_mappings = \
        new_mappings.loc[new_mappings[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name] != DEFAULT_NULL_VALUE]

    universe_nf_uuids_to_ea_guids_table = \
        concat(
            [
                universe_nf_uuids_to_ea_guids_table,
                new_mappings
            ])

    universe_nf_uuids_to_ea_guids_table = \
        universe_nf_uuids_to_ea_guids_table.drop_duplicates()

    universe_nf_uuids_to_ea_guids_table.reset_index(
        drop=True,
        inplace=True)

    return \
        universe_nf_uuids_to_ea_guids_table


def __get_secondary_to_primary_universe_nf_uuids_map(
        matched_by_ea_guid_nf_uuids_dataframe: DataFrame)\
        -> dict:
    matched_by_ea_guid_nf_uuids_dataframe_copy = \
        matched_by_ea_guid_nf_uuids_dataframe.copy()

    key_column = \
        NfColumnTypes.NF_UUIDS.column_name+DEFAULT_MASTER_TABLE_SUFFIX

    value_column = \
        NfColumnTypes.NF_UUIDS.column_name+DEFAULT_FOREIGN_TABLE_SUFFIX

    matched_by_ea_guid_nf_uuids_dataframe_copy = \
        matched_by_ea_guid_nf_uuids_dataframe_copy[
            [
                key_column,
                value_column
            ]]

    matched_by_ea_guid_nf_uuids_dataframe_copy.dropna(
        inplace=True)

    secondary_to_primary_universe_nf_uuids_map = \
        matched_by_ea_guid_nf_uuids_dataframe_copy.set_index(key_column)[value_column].to_dict()

    return \
        secondary_to_primary_universe_nf_uuids_map
