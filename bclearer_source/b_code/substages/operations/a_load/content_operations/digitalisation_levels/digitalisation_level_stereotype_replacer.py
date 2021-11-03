from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame

from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.substages.operations.b_evolve.common.digitalisation_level_stereotypes_usages_getter import \
    get_digitalisation_level_stereotypes_usages
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import \
    create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import \
    update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary


def replace_digitalisation_level_stereotype(
        nf_ea_com_universe: NfEaComUniverses,
        digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects) \
        -> None:
    current_digitalisation_level_stereotype_usages = \
        get_digitalisation_level_stereotypes_usages(
            nf_ea_com_universe=nf_ea_com_universe)

    __delete_current_digitalisation_level_stereotype_usages(
        nf_ea_com_universe=nf_ea_com_universe)

    __add_replacement_digitalisation_level_stereotype_usages(
        nf_ea_com_universe=nf_ea_com_universe,
        digitalisation_level_stereotype=digitalisation_level_stereotype,
        digitalisation_level_stereotype_usages_to_replace=current_digitalisation_level_stereotype_usages)


def __delete_current_digitalisation_level_stereotype_usages(
        nf_ea_com_universe: NfEaComUniverses):
    digitalisation_level_stereotype_ea_guids = \
        DigitalisationLevelStereotypeMatchedEaObjects.get_ea_guids()

    ea_stereotypes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()

    digitalisation_level_stereotypes = \
        ea_stereotypes[ea_stereotypes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name].isin(
            digitalisation_level_stereotype_ea_guids)]

    digitalisation_level_stereotypes_nf_uuids = \
        set(
            digitalisation_level_stereotypes[NfColumnTypes.NF_UUIDS.column_name])

    ea_stereotype_usages = \
        nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.STEREOTYPE_USAGE]

    stereotype_usages_to_keep = \
        ea_stereotype_usages[
            ~ea_stereotype_usages['stereotype_nf_uuids'].isin(digitalisation_level_stereotypes_nf_uuids)]

    nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.STEREOTYPE_USAGE] = \
        stereotype_usages_to_keep


def __add_replacement_digitalisation_level_stereotype_usages(
        nf_ea_com_universe: NfEaComUniverses,
        digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects,
        digitalisation_level_stereotype_usages_to_replace: DataFrame):
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)

    digitalisation_level_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=digitalisation_level_stereotype.ea_guid)

    classifier_digitalisation_level_stereotyped_nf_uuids = \
        set(
            digitalisation_level_stereotype_usages_to_replace[NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name])

    for ea_classifier_nf_uuid in classifier_digitalisation_level_stereotyped_nf_uuids:
        add_new_stereotype_usage_to_dictionary(
            new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
            client_nf_uuid=ea_classifier_nf_uuid,
            client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)
