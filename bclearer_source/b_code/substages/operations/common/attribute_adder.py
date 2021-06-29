from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes


def add_new_attribute_to_dictionary(
        new_ea_attributes_dictionary: dict,
        name_object_nf_uuid: str,
        attribute_value: str,
        attribute_name: str,
        attribute_type_nf_uuid: str) \
        -> str:
    attribute_nf_uuid = \
        create_new_uuid()

    attribute_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=attribute_nf_uuid)

    new_ea_attribute_dictionary = \
        {
            NfColumnTypes.NF_UUIDS.column_name: attribute_nf_uuid,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name: attribute_value,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name: name_object_nf_uuid,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name: attribute_type_nf_uuid,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name: 'Public',
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: attribute_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: attribute_ea_guid
        }

    new_ea_attributes_dictionary[attribute_nf_uuid] = \
        new_ea_attribute_dictionary

    return \
        attribute_nf_uuid
