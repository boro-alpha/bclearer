from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses

from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import \
    create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.new_stereotype_to_dictionary_adder import \
    add_new_stereotype_to_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import \
    update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary


def add_default_digitalisation_level_stereotype(
        nf_ea_com_universe: NfEaComUniverses,
        default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects) \
        -> None:
    __add_streotypes_if_required(
        nf_ea_com_universe=nf_ea_com_universe)

    __add_stereotype_usage(
        nf_ea_com_universe=nf_ea_com_universe,
        default_digitalisation_level_stereotype=default_digitalisation_level_stereotype)


def __add_streotypes_if_required(
        nf_ea_com_universe: NfEaComUniverses) \
        -> None:
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    ea_stereotypes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()

    ea_stereotype_ea_guids = \
        set(
            ea_stereotypes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name])

    for digitalisation_level_stereotype_matched_ea_object in DigitalisationLevelStereotypeMatchedEaObjects:
        __add_stereotype_if_required(
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            digitalisation_level_stereotype_matched_ea_object=digitalisation_level_stereotype_matched_ea_object,
            ea_stereotype_ea_guids=ea_stereotype_ea_guids)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __add_stereotype_if_required(
        new_ea_objects_dictionary: dict,
        digitalisation_level_stereotype_matched_ea_object: DigitalisationLevelStereotypeMatchedEaObjects,
        ea_stereotype_ea_guids: set) \
        -> None:
    if digitalisation_level_stereotype_matched_ea_object.ea_guid in ea_stereotype_ea_guids:
        return

    add_new_stereotype_to_dictionary(
        new_stereotype_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_STEREOTYPES],
        stereotype_ea_guid=digitalisation_level_stereotype_matched_ea_object.ea_guid,
        stereotype_name=digitalisation_level_stereotype_matched_ea_object.object_name,
        stereotype_applies_to='class',
        stereotype_style=digitalisation_level_stereotype_matched_ea_object.style)


def __add_stereotype_usage(
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

    ea_classifiers = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    ea_classifier_nf_uuids = \
        set(
            ea_classifiers[NfColumnTypes.NF_UUIDS.column_name])

    for ea_classifier_nf_uuid in ea_classifier_nf_uuids:
        add_new_stereotype_usage_to_dictionary(
            new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
            client_nf_uuid=ea_classifier_nf_uuid,
            client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            stereotype_nf_uuid=default_digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)
