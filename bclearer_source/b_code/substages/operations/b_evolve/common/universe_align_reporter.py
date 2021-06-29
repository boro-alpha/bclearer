from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes


def report_universes_with_different_collection_types(
        collection_types_in_primary_universe: set,
        collection_types_in_aligned_universe: set):
    primary_to_aligned_delta = \
        collection_types_in_primary_universe.difference(
            collection_types_in_aligned_universe)

    aligned_to_primary_delta = \
        collection_types_in_aligned_universe.difference(
            collection_types_in_primary_universe)

    log_message(
        message='Universes cannot be fully aligned because they keep different collections.')

    if len(primary_to_aligned_delta) > 0:
        log_message(
            message='Primary minus aligned ' + repr(primary_to_aligned_delta))

    if len(aligned_to_primary_delta) > 0:
        log_message(
            message='Aligned minus primary ' + repr(aligned_to_primary_delta))


def report_collection_with_different_columns(
        primary_universe_collection_columns: set,
        aligned_universe_collection_columns: set,
        collection_type: NfEaComCollectionTypes):
    primary_to_aligned_delta = \
        primary_universe_collection_columns.difference(
            aligned_universe_collection_columns)

    aligned_to_primary_delta = \
        aligned_universe_collection_columns.difference(
            primary_universe_collection_columns)

    log_message(
        message=collection_type.collection_name + ' collection type has different columns in the universes being merged.')

    if len(primary_to_aligned_delta) > 0:
        log_message(
            message='Primary minus aligned ' + repr(primary_to_aligned_delta))

    if len(aligned_to_primary_delta) > 0:
        log_message(
            message='Aligned minus primary ' + repr(aligned_to_primary_delta))
