from bclearer_source.b_code.substages.operations.b_evolve.common.universes_merge_registers import UniversesMergeRegisters
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_ea_com_collection_processes.universes_concatenator import concat_universe_collections
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def merge_universes(
        content_1_universe: NfEaComUniverses,
        content_2_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        context=str()) \
        -> NfEaComUniverses:
    __run_input_checks()

    output_universe = \
        __run_operation(
            content_1_universe=content_1_universe,
            content_2_universe=content_2_universe,
            output_universe=output_universe,
            context=context)

    return \
        output_universe


def __run_input_checks():
    pass


def __run_operation(
        content_1_universe: NfEaComUniverses,
        content_2_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        context: str) \
        -> NfEaComUniverses:
    log_message(
        message='CONTENT OPERATION: Merge universes - ' +
                content_1_universe.ea_repository.short_name + ' + ' +
                content_2_universe.ea_repository.short_name + ' - started')

    universes_merge_register = \
        UniversesMergeRegisters(
            universe_1=content_1_universe,
            universe_2=content_2_universe,
            context=context)

    common_collection_types, universe_1_surplus_collection_types, universe_2_surplus_collection_types = \
        __get_collection_types_distribution_over_universes(
            content_1_universe=content_1_universe,
            content_2_universe=content_2_universe)

    for collection_type in common_collection_types:
        concat_universe_collections(
            collection_type=collection_type,
            universe_merge_register=universes_merge_register,
            output_universe=output_universe)

    __add_collections(
        input_universe=content_1_universe,
        output_universe=output_universe,
        collection_types=universe_1_surplus_collection_types)

    __add_collections(
        input_universe=content_2_universe,
        output_universe=output_universe,
        collection_types=universe_2_surplus_collection_types)

    log_message(
        message='CONTENT OPERATION: Merge universes - ' +
                content_1_universe.ea_repository.short_name + ' + ' +
                content_2_universe.ea_repository.short_name + ' - finished')

    return \
        output_universe


def __get_collection_types_distribution_over_universes(
        content_1_universe: NfEaComUniverses,
        content_2_universe: NfEaComUniverses) \
        -> tuple:
    set_of_content_1_collection_types = \
        set(content_1_universe.nf_ea_com_registry.dictionary_of_collections.keys())

    set_of_content_2_collection_types = \
        set(content_2_universe.nf_ea_com_registry.dictionary_of_collections.keys())

    common_collection_types = \
        set_of_content_1_collection_types.intersection(
            set_of_content_2_collection_types)

    universe_1_surplus_collection_types = \
        set_of_content_1_collection_types.difference(
            set_of_content_2_collection_types)

    universe_2_surplus_collection_types = \
        set_of_content_2_collection_types.difference(
            set_of_content_1_collection_types)

    return \
        common_collection_types, universe_1_surplus_collection_types, universe_2_surplus_collection_types


def __add_collections(
        input_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        collection_types: set):
    for collection_type in collection_types:
        output_universe.nf_ea_com_registry.dictionary_of_collections[collection_type] = \
            input_universe.nf_ea_com_registry.dictionary_of_collections[collection_type]
