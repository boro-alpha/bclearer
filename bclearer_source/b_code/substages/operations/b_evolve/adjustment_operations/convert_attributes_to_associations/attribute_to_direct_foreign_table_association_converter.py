from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import \
    get_tuple_attribute_value_if_required
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import \
    EaAssociationDirectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes

from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.association_from_attribute_creator import \
    create_association_from_attribute


def convert_attribute_to_direct_foreign_table_association(
        attribute_to_convert_tuple: tuple,
        new_classifiers_dictionary: dict,
        new_connectors_dictionary: dict,
        direction: EaAssociationDirectionTypes) \
        -> tuple:
    new_connectors_dictionary = \
        __add_association(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            direction=direction,
            new_connectors_dictionary=new_connectors_dictionary)

    return \
        new_classifiers_dictionary, \
        new_connectors_dictionary


def __add_association(
        attribute_to_convert_tuple: tuple,
        direction: EaAssociationDirectionTypes,
        new_connectors_dictionary: dict) \
        -> dict:
    type_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name)

    attribute_name = \
        get_tuple_attribute_value_if_required(
            owning_tuple=attribute_to_convert_tuple,
            attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name)

    association_dictionary = \
        create_association_from_attribute(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            direction=direction,
            type_nf_uuid=type_nf_uuid,
            attribute_name=attribute_name)

    association_nf_uuid = \
        association_dictionary[NfColumnTypes.NF_UUIDS.column_name]

    new_connectors_dictionary[association_nf_uuid] = \
        association_dictionary

    return \
        new_connectors_dictionary
