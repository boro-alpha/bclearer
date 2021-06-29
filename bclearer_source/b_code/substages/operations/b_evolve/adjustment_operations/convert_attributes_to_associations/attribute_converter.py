from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.association_from_attribute_creator import create_association_from_attribute
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.dependency_from_attribute_creator import create_dependency_from_attribute
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.type_from_attribute_creator import create_type_from_attribute
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import EaAssociationDirectionTypes


def convert_attribute(
        attribute_to_convert_tuple: tuple,
        new_classifiers_dictionary: dict,
        new_connectors_dictionary: dict,
        direction: EaAssociationDirectionTypes,
        package_nf_uuid: str) \
        -> tuple:
    type_nf_uuid, new_classifiers_dictionary = \
        __add_type(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            package_nf_uuid=package_nf_uuid,
            new_classifiers_dictionary=new_classifiers_dictionary)

    new_connectors_dictionary = \
        __add_association(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            direction=direction,
            type_nf_uuid=type_nf_uuid,
            new_connectors_dictionary=new_connectors_dictionary)

    new_connectors_dictionary = \
        __add_dependency(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            type_nf_uuid=type_nf_uuid,
            new_connectors_dictionary=new_connectors_dictionary)

    return \
        new_classifiers_dictionary, \
        new_connectors_dictionary


def __add_type(
        attribute_to_convert_tuple: tuple,
        package_nf_uuid: str,
        new_classifiers_dictionary: dict) \
        -> tuple:
    type_dictionary = \
        create_type_from_attribute(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            package_nf_uuid=package_nf_uuid)

    type_nf_uuid = \
        type_dictionary[NfColumnTypes.NF_UUIDS.column_name]

    new_classifiers_dictionary[type_nf_uuid] = \
        type_dictionary

    return \
        type_nf_uuid, \
        new_classifiers_dictionary


def __add_association(
        attribute_to_convert_tuple: tuple,
        direction: EaAssociationDirectionTypes,
        type_nf_uuid: str,
        new_connectors_dictionary: dict) \
        -> dict:
    association_dictionary = \
        create_association_from_attribute(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            direction=direction,
            type_nf_uuid=type_nf_uuid)

    association_nf_uuid = \
        association_dictionary[NfColumnTypes.NF_UUIDS.column_name]

    new_connectors_dictionary[association_nf_uuid] =\
        association_dictionary

    return \
        new_connectors_dictionary


def __add_dependency(
        attribute_to_convert_tuple: tuple,
        type_nf_uuid: str,
        new_connectors_dictionary: dict) \
        -> dict:
    generalisation_dictionary = \
        create_dependency_from_attribute(
            attribute_to_convert_tuple=attribute_to_convert_tuple,
            type_nf_uuid=type_nf_uuid)

    association_nf_uuid = \
        generalisation_dictionary[NfColumnTypes.NF_UUIDS.column_name]

    new_connectors_dictionary[association_nf_uuid] =\
        generalisation_dictionary

    return \
        new_connectors_dictionary
