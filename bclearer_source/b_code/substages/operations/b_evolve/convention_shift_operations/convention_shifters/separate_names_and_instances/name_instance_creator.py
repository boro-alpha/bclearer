from bclearer_source.b_code.common_knowledge.bclearer_additional_column_types import BclearerAdditionalColumnTypes
from bclearer_source.b_code.common_knowledge.bclearer_constants import NAME_EXEMPLAR_ATTRIBUTE_NAME
from bclearer_source.b_code.substages.operations.common.attribute_adder import add_new_attribute_to_dictionary
from bclearer_source.b_code.substages.operations.common.class_adder import add_new_class_to_dictionary
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def create_name_instance(
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        ea_attribute_tuple: tuple,
        name_instance_type_nf_uuid: str,
        name_types_instances_stereotype_nf_uuid: str):
    attributed_object_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name)

    attributed_object_name = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=BclearerAdditionalColumnTypes.OWNING_OBJECT_NAMES.column_name)

    name_instance_name = \
        attributed_object_name + ' Instance'

    name_instance_nf_uuid = \
        add_new_class_to_dictionary(
            new_classifier_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS],
            package_nf_uuid=package_nf_uuid,
            class_name=name_instance_name)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_instance_nf_uuid,
        place_2_nf_uuid=name_instance_type_nf_uuid,
        connector_type=EaConnectorTypes.DEPENDENCY)

    association_nf_uuid = \
        add_new_connector_to_dictionary(
            new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
            place_1_nf_uuid=name_instance_nf_uuid,
            place_2_nf_uuid=attributed_object_nf_uuid,
            connector_type=EaConnectorTypes.ASSOCIATION)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=association_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
        stereotype_nf_uuid=name_types_instances_stereotype_nf_uuid)

    attribute_value = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name)

    attribute_type_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name)

    add_new_attribute_to_dictionary(
        new_ea_attributes_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_ATTRIBUTES],
        name_object_nf_uuid=name_instance_nf_uuid,
        attribute_value=attribute_value,
        attribute_name=NAME_EXEMPLAR_ATTRIBUTE_NAME,
        attribute_type_nf_uuid=attribute_type_nf_uuid)
