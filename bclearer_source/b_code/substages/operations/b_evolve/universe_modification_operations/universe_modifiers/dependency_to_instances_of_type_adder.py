from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.instances_nf_uuids_getter import \
    get_instances_nf_uuids_of_matched_type
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import \
    create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import \
    update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def add_dependency_to_instances_of_type(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        matched_target_object: MatchedEaObjects,
        matched_source_objects_type: MatchedEaObjects):
    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    matched_target_object_type_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=content_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=matched_target_object.ea_guid)

    classifiers_instances_of_matched_source_objects_type = \
        get_instances_nf_uuids_of_matched_type(
            nf_ea_com_universe=content_universe,
            matched_type=matched_source_objects_type)

    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    for instance_of_source_objects_type in classifiers_instances_of_matched_source_objects_type:
        add_new_connector_to_dictionary(
            new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
            place_1_nf_uuid=instance_of_source_objects_type,
            place_2_nf_uuid=matched_target_object_type_nf_uuid,
            connector_type=EaConnectorTypes.DEPENDENCY)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=output_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)
