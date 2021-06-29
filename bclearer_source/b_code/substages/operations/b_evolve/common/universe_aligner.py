from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from pandas import DataFrame
from bclearer_source.b_code.substages.operations.b_evolve.common.universe_align_reporter import report_universes_with_different_collection_types, report_collection_with_different_columns
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_uuid_mapping_processes.merged_collection_nf_uuids_replacer import replace_nf_uuids_in_collection
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_uuid_mapping_processes.nf_uuid_mapping_creator import create_aligned_to_primary_universe_nf_uuids_map
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes


def align_universes(
        universe_merge_register,
        context: str):
    primary_universe_name = \
        universe_merge_register.primary_universe.ea_repository.short_name

    aligned_universe_name = \
        universe_merge_register.aligned_universe.ea_repository.short_name

    log_message(
        message='In context ' + context + ' two universes are nf uuid aligned: ' + primary_universe_name + ' as primary and ' + aligned_universe_name + ' as aligned')

    alignment_scope = \
        __set_alignment_scope(
            universe_merge_register=universe_merge_register)

    __align_universe_registries(
        alignment_scope=alignment_scope,
        universe_merge_register=universe_merge_register)


def __set_alignment_scope(
        universe_merge_register) \
        -> set:
    collection_types_in_primary_universe = \
        set(universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections.keys())

    collection_types_in_aligned_universe = \
        set(universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections.keys())

    if not collection_types_in_primary_universe == collection_types_in_aligned_universe:
        report_universes_with_different_collection_types(
            collection_types_in_primary_universe=collection_types_in_primary_universe,
            collection_types_in_aligned_universe=collection_types_in_aligned_universe)

    return \
        collection_types_in_primary_universe.intersection(
            collection_types_in_aligned_universe)


def __align_universe_registries(
        universe_merge_register,
        alignment_scope: set):
    for collection_type in alignment_scope:
        __check_column_consistency_in_alignment(
            collection_type=collection_type,
            universe_merge_register=universe_merge_register)

    universe_merge_register.aligned_to_primary_universe_nf_uuids_map = \
        create_aligned_to_primary_universe_nf_uuids_map(
            primary_universe=universe_merge_register.primary_universe,
            aligned_universe=universe_merge_register.aligned_universe)

    for collection_type, collection in universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections.items():
        __align_collection_in_universe(
            collection=collection,
            collection_type=collection_type,
            universe_merge_register=universe_merge_register)


def __check_column_consistency_in_alignment(
        universe_merge_register,
        collection_type: NfEaComCollectionTypes):
    primary_universe_collection = \
        universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections[collection_type]

    aligned_universe_collection = \
        universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections[collection_type]

    primary_universe_collection_columns = \
        set(primary_universe_collection.columns)

    aligned_universe_collection_columns = \
        set(aligned_universe_collection.columns)

    if not primary_universe_collection_columns == aligned_universe_collection_columns:
        report_collection_with_different_columns(
            primary_universe_collection_columns=primary_universe_collection_columns,
            aligned_universe_collection_columns=aligned_universe_collection_columns,
            collection_type=collection_type)


def __align_collection_in_universe(
        universe_merge_register,
        collection: DataFrame,
        collection_type: NfEaComCollectionTypes):
    updated_collection = \
        collection.copy()

    for column in collection.columns:
        updated_collection = \
            replace_nf_uuids_in_collection(
                column_name=column,
                nf_uuid_mapping_dictionary=universe_merge_register.aligned_to_primary_universe_nf_uuids_map,
                collection=updated_collection)

    universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections[collection_type] = \
        updated_collection
