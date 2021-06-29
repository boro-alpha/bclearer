from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def has_classifier_ea_guid_attribute_type_name_and_value(
        content_universe: NfEaComUniverses,
        classifier_ea_guid: str,
        attribute_type_name: str,
        attribute_value: str) \
        -> bool:
    content_universe_ea_classifiers = \
        content_universe.nf_ea_com_registry.get_ea_classifiers()

    classifier_list_of_attribute_nf_uuids = \
        __get_classifier_list_of_attribute_nf_uuids(
            content_universe_ea_classifiers=content_universe_ea_classifiers,
            classifier_ea_guid=classifier_ea_guid)

    classifier_ea_guid_has_attribute_type_name_and_value = \
        False

    content_universe_ea_attributes = \
        content_universe.nf_ea_com_registry.get_ea_attributes()

    for attribute_nf_uuid in classifier_list_of_attribute_nf_uuids:
        classifier_ea_guid_has_attribute_type_name_and_value = \
            __check_attribute_and_type_is_a_match(
                content_universe_ea_attributes=content_universe_ea_attributes,
                content_universe_ea_classifiers=content_universe_ea_classifiers,
                attribute_value=attribute_value,
                attribute_type_name=attribute_type_name,
                attribute_nf_uuid=attribute_nf_uuid)

        if classifier_ea_guid_has_attribute_type_name_and_value:
            return \
                True

    return \
        classifier_ea_guid_has_attribute_type_name_and_value


def __get_classifier_list_of_attribute_nf_uuids(
        content_universe_ea_classifiers: DataFrame,
        classifier_ea_guid: str) \
        -> list:
    ea_guid_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name

    all_component_ea_attributes_column_name = \
        NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES.column_name

    classifier_list_of_attribute_nf_uuids = \
        content_universe_ea_classifiers[
            content_universe_ea_classifiers[ea_guid_column_name] == classifier_ea_guid][
            all_component_ea_attributes_column_name].tolist()[0]

    return \
        classifier_list_of_attribute_nf_uuids


def __check_attribute_and_type_is_a_match(
        content_universe_ea_attributes: DataFrame,
        attribute_nf_uuid: str,
        content_universe_ea_classifiers: DataFrame,
        attribute_value: str,
        attribute_type_name: str) \
        -> bool:
    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    ea_object_name_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name

    classifying_ea_classifier_column_name = \
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name

    current_attribute_dataframe_slice = \
        content_universe_ea_attributes[
            content_universe_ea_attributes[nf_uuids_column_name] == attribute_nf_uuid]

    if current_attribute_dataframe_slice.empty:
        return False

    current_attribute_value = \
        current_attribute_dataframe_slice[ea_object_name_column_name].values[0]

    current_attribute_type_nf_uuid_string = \
        current_attribute_dataframe_slice[classifying_ea_classifier_column_name].values[0]

    current_attribute_type_name_result = \
        content_universe_ea_classifiers[
            content_universe_ea_classifiers[nf_uuids_column_name] == current_attribute_type_nf_uuid_string][
            ea_object_name_column_name]

    if not current_attribute_type_name_result.empty:
        current_attribute_type_name = \
            current_attribute_type_name_result.values[0]

        if attribute_value == current_attribute_value and attribute_type_name == current_attribute_type_name:
            return \
                True

    return \
        False
