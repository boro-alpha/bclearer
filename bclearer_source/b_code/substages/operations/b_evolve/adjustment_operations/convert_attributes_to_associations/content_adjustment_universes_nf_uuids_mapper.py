from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.constants.standard_constants import DEFAULT_MASTER_TABLE_SUFFIX
from nf_common_source.code.constants.standard_constants import DEFAULT_FOREIGN_TABLE_SUFFIX
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.dataframe_service.dataframe_mergers import inner_merge_dataframes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def get_mapped_nf_uuid_from_mapped_universe(
        source_nf_uuid: str,
        source_universe_collection_dictionary: dict,
        mapped_universe_collection_dictionary: dict) \
        -> str:
    ea_guid_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name

    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    nf_uuids_source_universe_column_name = \
        'nf_uuids_source_universe'

    nf_uuids_mapped_universe_column_name = \
        'nf_uuids_mapped_universe'

    ea_guids_to_nf_uuids_source_universe = \
        source_universe_collection_dictionary[NfEaComCollectionTypes.THIN_EA_EXPLICIT_OBJECTS][[
            ea_guid_column_name,
            nf_uuids_column_name]]

    ea_guids_to_nf_uuids_source_universe.rename(
        columns={nf_uuids_column_name: nf_uuids_source_universe_column_name},
        inplace=True)

    ea_guids_to_nf_uuids_mapped_universe = \
        mapped_universe_collection_dictionary[NfEaComCollectionTypes.THIN_EA_EXPLICIT_OBJECTS][[
            ea_guid_column_name,
            nf_uuids_column_name]]

    ea_guids_to_nf_uuids_mapped_universe.rename(
        columns={nf_uuids_column_name: nf_uuids_mapped_universe_column_name},
        inplace=True)

    ea_guids_to_nf_uuids_map = \
        inner_merge_dataframes(
            master_dataframe=ea_guids_to_nf_uuids_source_universe,
            master_dataframe_key_columns=[ea_guid_column_name],
            merge_suffixes=[DEFAULT_MASTER_TABLE_SUFFIX, DEFAULT_FOREIGN_TABLE_SUFFIX],
            foreign_key_dataframe=ea_guids_to_nf_uuids_mapped_universe,
            foreign_key_dataframe_fk_columns=[ea_guid_column_name],
            foreign_key_dataframe_other_column_rename_dictionary=
            {
                nf_uuids_mapped_universe_column_name: nf_uuids_mapped_universe_column_name
            })

    mapped_nf_uuids_keyed_on_source_nf_uuids_dictionary = {}

    for row_tuple in ea_guids_to_nf_uuids_map.itertuples():
        row_source_nf_uuid = \
            getattr(
                row_tuple,
                'nf_uuids_source_universe')

        row_mapped_nf_uuid = \
            getattr(
                row_tuple,
                'nf_uuids_mapped_universe')

        mapped_nf_uuids_keyed_on_source_nf_uuids_dictionary[row_source_nf_uuid] = \
            row_mapped_nf_uuid

    if source_nf_uuid in mapped_nf_uuids_keyed_on_source_nf_uuids_dictionary:
        return \
            mapped_nf_uuids_keyed_on_source_nf_uuids_dictionary[source_nf_uuid]

    return \
        DEFAULT_NULL_VALUE
