import pandas

from bclearer_source.b_code.common_knowledge.attribute_to_associations_operation_subtypes import \
    AttributeToAssociationOperationSubtypes
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.attribute_to_direct_foreign_table_association_converter import \
    convert_attribute_to_direct_foreign_table_association
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.attribute_to_subtype_foreign_table_association_converter import convert_attribute_to_subtype_foreign_table_association
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import EaAssociationDirectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def convert_attributes(
        output_universe: NfEaComUniverses,
        attributes_to_convert: DataFrame,
        direction: EaAssociationDirectionTypes,
        package_nf_uuid: str,
        attribute_to_association_operation_subtype: AttributeToAssociationOperationSubtypes) \
        -> None:
    new_classifiers_dictionary, new_connectors_dictionary = \
        __get_new_objects(
            attributes_to_convert=attributes_to_convert,
            direction=direction,
            package_nf_uuid=package_nf_uuid,
            attribute_to_association_operation_subtype=attribute_to_association_operation_subtype)

    output_collections_dictionary = \
        output_universe.nf_ea_com_registry.dictionary_of_collections

    __update_nf_ea_com_dictionary(
        ea_object_map=new_classifiers_dictionary,
        nf_ea_com_dictionary=output_collections_dictionary,
        nf_ea_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS)

    __update_nf_ea_com_dictionary(
        ea_object_map=new_connectors_dictionary,
        nf_ea_com_dictionary=output_collections_dictionary,
        nf_ea_collection_type=NfEaComCollectionTypes.EA_CONNECTORS)


def __get_new_objects(
        attributes_to_convert: DataFrame,
        direction: EaAssociationDirectionTypes,
        package_nf_uuid: str,
        attribute_to_association_operation_subtype: AttributeToAssociationOperationSubtypes) \
        -> tuple:
    new_classifiers_dictionary = \
        {}

    new_connectors_dictionary = \
        {}

    # TODO: Add the cardinality to the connector's data
    for attribute_to_convert_tuple in attributes_to_convert.itertuples():
        new_classifiers_dictionary, new_connectors_dictionary = \
            __convert_attribute_to_association_by_subtype(
                attribute_to_convert_tuple=attribute_to_convert_tuple,
                new_classifiers_dictionary=new_classifiers_dictionary,
                new_connectors_dictionary=new_connectors_dictionary,
                direction=direction,
                package_nf_uuid=package_nf_uuid,
                attribute_to_association_operation_subtype=attribute_to_association_operation_subtype)

    return \
        new_classifiers_dictionary, new_connectors_dictionary


def __convert_attribute_to_association_by_subtype(
        attribute_to_convert_tuple: tuple,
        direction: EaAssociationDirectionTypes,
        new_classifiers_dictionary: dict,
        new_connectors_dictionary: dict,
        package_nf_uuid: str,
        attribute_to_association_operation_subtype: AttributeToAssociationOperationSubtypes) \
        -> tuple:
    if attribute_to_association_operation_subtype is AttributeToAssociationOperationSubtypes.SUBTYPE_OF_FOREIGN_TABLE:
        new_classifiers_dictionary, new_connectors_dictionary = \
            convert_attribute_to_subtype_foreign_table_association(
                attribute_to_convert_tuple=attribute_to_convert_tuple,
                new_classifiers_dictionary=new_classifiers_dictionary,
                new_connectors_dictionary=new_connectors_dictionary,
                direction=direction,
                package_nf_uuid=package_nf_uuid)

    elif attribute_to_association_operation_subtype is AttributeToAssociationOperationSubtypes.DIRECT_FOREIGN_TABLE:
        new_classifiers_dictionary, new_connectors_dictionary = \
            convert_attribute_to_direct_foreign_table_association(
                attribute_to_convert_tuple=attribute_to_convert_tuple,
                new_classifiers_dictionary=new_classifiers_dictionary,
                new_connectors_dictionary=new_connectors_dictionary,
                direction=direction)

    return \
        new_classifiers_dictionary, new_connectors_dictionary


def __update_nf_ea_com_dictionary(
        nf_ea_com_dictionary: dict,
        ea_object_map: dict,
        nf_ea_collection_type: NfEaComCollectionTypes):
    nf_ea_collection = \
        nf_ea_com_dictionary[nf_ea_collection_type]

    converted_nf_ea_collection = \
        pandas.DataFrame.from_dict(
            data=ea_object_map,
            orient='index')

    all_ea_objects = \
        pandas.concat(
            objs=[nf_ea_collection, converted_nf_ea_collection],
            ignore_index=True,
            verify_integrity=False)

    nf_ea_com_dictionary[nf_ea_collection_type] = \
        all_ea_objects
