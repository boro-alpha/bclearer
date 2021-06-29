from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def create_type_from_attribute(
        attribute_to_convert_tuple: tuple,
        package_nf_uuid: str) \
        -> dict:
    new_type_nf_uuid = \
        create_new_uuid()

    new_type_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=new_type_nf_uuid)

    new_type_name = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name)

    ea_classifier_dictionary = \
        {
            NfColumnTypes.NF_UUIDS.column_name: new_type_nf_uuid,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: new_type_ea_guid,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: new_type_name,
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name: EaElementTypes.CLASS.type_name,
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name: package_nf_uuid
        }

    return \
        ea_classifier_dictionary
