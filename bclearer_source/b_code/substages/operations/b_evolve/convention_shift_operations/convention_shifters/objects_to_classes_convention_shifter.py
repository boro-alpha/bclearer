from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def shift_convention_objects_to_classes(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    __run_input_checks()

    __run_operation(
        content_universe=content_universe,
        output_universe=output_universe)


def __run_operation(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    log_message(
        message='CONVENTION SHIFT OPERATION: Shift objects to classes - started')

    content_collections_dictionary = \
        content_universe.nf_ea_com_registry.dictionary_of_collections

    for content_collection_type, content_collection_table in content_collections_dictionary.items():
        __process_content_collection(
            content_collection_type=content_collection_type,
            content_collection_table=content_collection_table,
            output_universe=output_universe)

    log_message(
        message='CONVENTION SHIFT OPERATION: Shift objects to classes - finished')


def __run_input_checks():
    pass


def __process_content_collection(
        content_collection_type: NfEaComCollectionTypes,
        content_collection_table: DataFrame,
        output_universe: NfEaComUniverses) \
        -> None:
    output_collections_dictionary = \
        output_universe.nf_ea_com_registry.dictionary_of_collections

    if content_collection_type == NfEaComCollectionTypes.EA_CLASSIFIERS:
        __convert_objects_to_classes(
            output_collections_dictionary=output_collections_dictionary,
            ea_classifiers=content_collection_table)

    else:
        output_collections_dictionary[content_collection_type] = \
            content_collection_table


def __convert_objects_to_classes(
        output_collections_dictionary: dict,
        ea_classifiers: DataFrame) \
        -> None:
    ea_object_type_column_name = \
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name

    number_of_objects_before_conversion = \
        len(ea_classifiers[ea_classifiers[ea_object_type_column_name] == EaElementTypes.OBJECT.type_name].index)

    ea_classifiers[ea_object_type_column_name].replace(
        to_replace=EaElementTypes.OBJECT.type_name,
        value=EaElementTypes.CLASS.type_name,
        inplace=True)

    number_of_objects_after_conversion = \
        len(ea_classifiers[ea_classifiers[ea_object_type_column_name] == EaElementTypes.OBJECT.type_name].index)

    number_of_objects_converted_to_classes = \
        number_of_objects_before_conversion - number_of_objects_after_conversion

    log_message(
        message='CONVENTION SHIFT OPERATION: Shift objects to classes - Number of objects converted: ' +
                str(number_of_objects_converted_to_classes))

    output_collections_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS] = \
        ea_classifiers
