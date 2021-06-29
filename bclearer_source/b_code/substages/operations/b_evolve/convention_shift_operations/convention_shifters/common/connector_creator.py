from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def create_connector(
        new_ea_connectors_dictionary: dict,
        place_1_nf_uuid: str,
        place_2_nf_uuid: str,
        connector_name: str,
        connector_type: EaConnectorTypes) \
        -> str:
    new_connector_nf_uuid = \
        create_new_uuid()

    new_connector_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=new_connector_nf_uuid)

    nf_ea_com_universe_new_connector_row_dictionary = {
        NfColumnTypes.NF_UUIDS.column_name: new_connector_nf_uuid,
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: place_1_nf_uuid,
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: place_2_nf_uuid,
        NfEaComColumnTypes.CONNECTORS_DIRECTION_TYPE_NAME.column_name: 'Source -> Destination',
        NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name: connector_type.type_name,
        NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: connector_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: new_connector_ea_guid
    }

    new_ea_connectors_dictionary[len(new_ea_connectors_dictionary) + 1] = \
        nf_ea_com_universe_new_connector_row_dictionary

    return \
        new_connector_nf_uuid
