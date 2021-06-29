from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.substages.operations.common.class_adder import add_new_class_to_dictionary
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def create_name_instance_type(
        nf_ea_com_universe: NfEaComUniverses,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        name_object_name: str,
        naming_space_nf_uuid: str) \
        -> str:
    name_instance_type_nf_uuid = \
        add_new_class_to_dictionary(
            new_classifier_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS],
            package_nf_uuid=package_nf_uuid,
            class_name=name_object_name)

    name_instances_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=BclearerMatchedEaObjects.NAME_INSTANCES.ea_guid)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_instance_type_nf_uuid,
        place_2_nf_uuid=name_instances_nf_uuid,
        connector_type=EaConnectorTypes.GENERALIZATION)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_instance_type_nf_uuid,
        place_2_nf_uuid=naming_space_nf_uuid,
        connector_type=EaConnectorTypes.ASSOCIATION,
        connector_name=BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE.object_name)

    return \
        name_instance_type_nf_uuid
