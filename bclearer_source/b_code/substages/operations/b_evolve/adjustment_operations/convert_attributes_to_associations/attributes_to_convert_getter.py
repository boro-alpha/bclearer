from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.content_adjustment_universes_nf_uuids_mapper import get_mapped_nf_uuid_from_mapped_universe
from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def get_attributes_to_convert(
        content_universe: NfEaComUniverses,
        adjustment_universe: NfEaComUniverses) \
        -> DataFrame:
    content_collection_dictionary = \
        content_universe.nf_ea_com_registry.dictionary_of_collections

    adjustment_collection_dictionary = \
        adjustment_universe.nf_ea_com_registry.dictionary_of_collections

    adjustment_universe_ea_attributes_table = \
        adjustment_collection_dictionary[NfEaComCollectionTypes.EA_ATTRIBUTES]

    filter_columns = \
        [
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
            NfEaComColumnTypes.ATTRIBUTES_LOWER_BOUNDS.column_name,
            NfEaComColumnTypes.ATTRIBUTES_UPPER_BOUNDS.column_name]

    attribute_conversion_table = \
        adjustment_universe_ea_attributes_table.filter(
            items=filter_columns)

    attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name] = \
        adjustment_universe_ea_attributes_table[
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name].apply(
            lambda source_nf_uuid: get_mapped_nf_uuid_from_mapped_universe(
                source_nf_uuid=source_nf_uuid,
                source_universe_collection_dictionary=adjustment_collection_dictionary,
                mapped_universe_collection_dictionary=content_collection_dictionary))

    attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name] = \
        adjustment_universe_ea_attributes_table[
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name].apply(
            lambda source_nf_uuid: get_mapped_nf_uuid_from_mapped_universe(
                source_nf_uuid=source_nf_uuid,
                source_universe_collection_dictionary=adjustment_collection_dictionary,
                mapped_universe_collection_dictionary=content_collection_dictionary))

    cleaned_attribute_conversion_table = \
        __get_cleaned_attribute_conversion_table(
            attribute_conversion_table=attribute_conversion_table)

    return \
        cleaned_attribute_conversion_table


def __get_cleaned_attribute_conversion_table(
        attribute_conversion_table: DataFrame) \
        -> DataFrame:
    __log_failed_conversions(
        attribute_conversion_table=attribute_conversion_table)

    cleaned_attribute_conversion_table = \
        attribute_conversion_table.loc[
            attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name] != DEFAULT_NULL_VALUE]

    cleaned_attribute_conversion_table = \
        cleaned_attribute_conversion_table.loc[
            cleaned_attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name] != DEFAULT_NULL_VALUE]

    return \
        cleaned_attribute_conversion_table


def __log_failed_conversions(
        attribute_conversion_table: DataFrame) \
        -> None:
    attributes_with_no_attributed_object = \
        attribute_conversion_table.loc[
            attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name] == DEFAULT_NULL_VALUE]

    if not attributes_with_no_attributed_object.empty:
        for bad_attributed_objects_row in attributes_with_no_attributed_object.iterrows():
            log_message(
                message='Attribute with name: ' + str(bad_attributed_objects_row[1][1]) + ' - and EA GUID: ' +
                        str(bad_attributed_objects_row[1][0]) + ' - cannot be converted. It has no attributed object.')

    attributes_with_no_attribute_type = \
        attribute_conversion_table.loc[attribute_conversion_table[NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name] == DEFAULT_NULL_VALUE]

    if not attributes_with_no_attribute_type.empty:
        for bad_attribute_types_row in attributes_with_no_attribute_type.iterrows():
            log_message(
                message='Attribute with name: ' + str(bad_attribute_types_row[1][1]) + ' - and EA GUID: ' +
                        str(bad_attribute_types_row[1][0]) + ' - cannot be converted. It has no attribute type.')
