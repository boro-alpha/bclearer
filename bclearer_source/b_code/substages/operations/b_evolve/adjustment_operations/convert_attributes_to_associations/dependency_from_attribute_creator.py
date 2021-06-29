from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def create_dependency_from_attribute(
        attribute_to_convert_tuple: tuple,
        type_nf_uuid: str) \
        -> dict:
    dependency_nf_uuid = \
        create_new_uuid()

    dependency_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=dependency_nf_uuid)

    dependency_supplier_nf_uuid = \
        type_nf_uuid

    dependency_client_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name)

    ea_dependency_dictionary = \
        {
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: dependency_ea_guid,
            NfColumnTypes.NF_UUIDS.column_name: dependency_nf_uuid,
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: dependency_supplier_nf_uuid,
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: dependency_client_nf_uuid,
            NfEaComColumnTypes.CONNECTORS_DIRECTION_TYPE_NAME.column_name: 'Source -> Destination',
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: EaConnectorTypes.DEPENDENCY.type_name,
            NfEaComColumnTypes.CONNECTORS_SOURCE_CARDINALITY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.CONNECTORS_DEST_CARDINALITY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
            NfEaComColumnTypes.REPOSITORIED_OBJECTS_EA_REPOSITORY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: DEFAULT_NULL_VALUE
        }

    return \
        ea_dependency_dictionary
