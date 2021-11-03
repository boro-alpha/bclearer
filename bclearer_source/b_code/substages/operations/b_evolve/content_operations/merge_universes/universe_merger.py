from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes

from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.substages.operations.b_evolve.common.digitalisation_level_stereotypes_usages_getter import \
    get_digitalisation_level_stereotypes_usages
from bclearer_source.b_code.substages.operations.b_evolve.common.universes_merge_registers import UniversesMergeRegisters
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.nf_ea_com_collection_processes.universes_concatenator import concat_universe_collections
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses

from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import \
    create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import \
    update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary


def merge_universes(
        content_1_universe: NfEaComUniverses,
        content_2_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects,
        context=str()) \
        -> NfEaComUniverses:
    __run_input_checks()

    output_universe = \
        __run_operation(
            content_1_universe=content_1_universe,
            content_2_universe=content_2_universe,
            output_universe=output_universe,
            default_digitalisation_level_stereotype=default_digitalisation_level_stereotype,
            context=context)

    return \
        output_universe


def __run_input_checks():
    pass


def __run_operation(
        content_1_universe: NfEaComUniverses,
        content_2_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects,
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

    if default_digitalisation_level_stereotype:
        __add_default_digitalisation_level_stereotypes(
            nf_ea_com_universe=output_universe,
            default_digitalisation_level_stereotype=default_digitalisation_level_stereotype)

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


def __add_default_digitalisation_level_stereotypes(
        nf_ea_com_universe: NfEaComUniverses,
        default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects) \
        -> None:
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    default_digitalisation_level_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=default_digitalisation_level_stereotype.ea_guid)

    digitalisation_level_stereotypes_usages = \
        get_digitalisation_level_stereotypes_usages(
            nf_ea_com_universe=nf_ea_com_universe)

    classifier_digitalisation_level_stereotyped_nf_uuids = \
        set(
            digitalisation_level_stereotypes_usages[NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name])

    ea_classifiers =  \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    ea_classifiers_without_digitalisation_levels = \
        ea_classifiers[~ea_classifiers[NfColumnTypes.NF_UUIDS.column_name].isin(classifier_digitalisation_level_stereotyped_nf_uuids)]

    ea_classifiers_without_digitalisation_level_nf_uuids = \
        set(
            ea_classifiers_without_digitalisation_levels[NfColumnTypes.NF_UUIDS.column_name])

    for ea_classifier_nf_uuid in ea_classifiers_without_digitalisation_level_nf_uuids:
        add_new_stereotype_usage_to_dictionary(
            new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
            client_nf_uuid=ea_classifier_nf_uuid,
            client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            stereotype_nf_uuid=default_digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)
