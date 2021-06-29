from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import EaAssociationDirectionTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def create_association_from_attribute(
        attribute_to_convert_tuple: tuple,
        direction: EaAssociationDirectionTypes,
        type_nf_uuid: str) \
        -> dict:
    association_nf_uuid = \
        create_new_uuid()

    association_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=association_nf_uuid)
    
    association_owner_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name)

    if direction == EaAssociationDirectionTypes.FORWARD:
        association_client_nf_uuid = \
            type_nf_uuid
        
        association_supplier_nf_uuid = \
            association_owner_nf_uuid
    
    else:
        association_client_nf_uuid = \
            association_owner_nf_uuid

        association_supplier_nf_uuid = \
            type_nf_uuid

    association_client_cardinality = \
        __get_connector_client_cardinality(
            attribute_to_convert_tuple=attribute_to_convert_tuple)

    ea_association_dictionary = \
        {
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: association_ea_guid,
            NfColumnTypes.NF_UUIDS.column_name: association_nf_uuid,
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: association_supplier_nf_uuid,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: association_client_nf_uuid,
            NfEaComColumnTypes.CONNECTORS_DIRECTION_TYPE_NAME.column_name: 'Source -> Destination',
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: EaConnectorTypes.ASSOCIATION.type_name,
            NfEaComColumnTypes.CONNECTORS_SOURCE_CARDINALITY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.CONNECTORS_DEST_CARDINALITY.column_name: association_client_cardinality,
            NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
            NfEaComColumnTypes.REPOSITORIED_OBJECTS_EA_REPOSITORY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: DEFAULT_NULL_VALUE
        }

    return \
        ea_association_dictionary


def __get_connector_client_cardinality(
        attribute_to_convert_tuple: tuple) \
        -> str:
    attribute_lower_bound = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.ATTRIBUTES_LOWER_BOUNDS.column_name)

    attribute_upper_bound = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.ATTRIBUTES_UPPER_BOUNDS.column_name)

    if attribute_lower_bound != attribute_upper_bound:
        connector_client_cardinality = \
            attribute_lower_bound + '..' + attribute_upper_bound

    else:
        connector_client_cardinality = \
            attribute_lower_bound

    return \
        connector_client_cardinality
