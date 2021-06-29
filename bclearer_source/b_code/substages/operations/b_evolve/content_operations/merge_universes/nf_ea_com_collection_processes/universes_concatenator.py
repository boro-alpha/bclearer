from bclearer_source.b_code.substages.operations.b_evolve.common.universes_merge_registers import UniversesMergeRegisters
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_ea_com_collection_processes.collection_type_compliation_constants import LIST_OF_COLLECTION_TYPES_OF_OBJECTS_WITHOUT_EA_GUIDS
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import concat


def concat_universe_collections(
        collection_type: NfEaComCollectionTypes,
        universe_merge_register: UniversesMergeRegisters,
        output_universe: NfEaComUniverses):
    if not collection_type:
        log_message(
            message='CONTENT OPERATION: Concat universes - concatenating collections - No Collection type - Skipped')

        return

    log_message(
        message='CONTENT OPERATION: Concat universes - concatenating collections - ' +
                collection_type.collection_name)

    if collection_type in LIST_OF_COLLECTION_TYPES_OF_OBJECTS_WITHOUT_EA_GUIDS:
        concatenated_collection = \
            universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections[
                collection_type].copy()

    else:
        concatenated_collection = \
            concat(
                [
                    universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections[collection_type],
                    universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections[collection_type]
                ])

    concatenated_collection.reset_index(
        drop=True,
        inplace=True)

    if NfColumnTypes.NF_UUIDS.column_name in concatenated_collection.columns:
        concatenated_collection.drop_duplicates(
            subset=NfColumnTypes.NF_UUIDS.column_name,
            inplace=True)

    output_universe.nf_ea_com_registry.dictionary_of_collections[collection_type] = \
        concatenated_collection
