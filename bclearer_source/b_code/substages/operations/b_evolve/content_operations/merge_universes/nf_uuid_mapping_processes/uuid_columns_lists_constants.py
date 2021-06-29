from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes

LIST_OF_NF_UUID_COLUMN_NAMES = [
    NfColumnTypes.NF_UUIDS.column_name,
    NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name,
    NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name,
    NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name,
    NfEaComColumnTypes.CLASSIFIERS_CONTAINING_EA_ELEMENT.column_name,
    NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name,
    # It is used in the data both as uuid field and uuid list field
    NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
    # It is used in the data both as uuid field and uuid list field
    NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name,
    'provider',
    'dependent',
    'specialisation',
    'generalisation',
    'child',
    'parent',
    'ea_client',
    'ea_stereotype',
    NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name,
    NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name,
    'stereotype_nf_uuids'
]

LIST_OF_NF_UUID_LISTS_COLUMN_NAMES = [
    NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES.column_name,
    # It is used in the data both as uuid field and uuid list field
    NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name,
    # It is used in the data both as uuid field and uuid list field
    NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS,
    NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_OPERATIONS.column_name,
    NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS.column_name,
    NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS.column_name,
    NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name,
    NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name,
    'paths'
]
