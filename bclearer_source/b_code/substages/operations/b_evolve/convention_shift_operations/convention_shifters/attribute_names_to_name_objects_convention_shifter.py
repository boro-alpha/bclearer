from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.common_knowledge.bclearer_constants import NAME_INSTANCE_ATTRIBUTE_NAME
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.common.new_subpackage_creator import create_new_subpackage_if_not_exist
from bclearer_source.b_code.substages.operations.common.attribute_adder import add_new_attribute_to_dictionary
from bclearer_source.b_code.substages.operations.common.class_adder import add_new_class_to_dictionary
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def shift_convention_attribute_names_to_name_objects(
        content_universe: NfEaComUniverses,
        list_of_configuration_objects: list,
        output_universe: NfEaComUniverses) \
        -> NfEaComUniverses:
    log_message(
        message='CONVENTION SHIFT OPERATION: Extract attribute names to name objects - started')

    naming_space_instances_ea_guids = \
        [configuration_object.matched_naming_space_instance.ea_guid
         for configuration_object in list_of_configuration_objects]

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    output_universe_ea_classifiers = \
        output_universe.nf_ea_com_registry.get_ea_classifiers()

    output_universe_ea_attributes = \
        output_universe.nf_ea_com_registry.get_ea_attributes()

    naming_space_instances_nf_uuids = \
        output_universe_ea_classifiers[
            output_universe_ea_classifiers[
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name].isin(naming_space_instances_ea_guids)][
            NfColumnTypes.NF_UUIDS.column_name]

    output_universe_name_attributes = \
        output_universe_ea_attributes[
            output_universe_ea_attributes[
                NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name].isin(naming_space_instances_nf_uuids)]

    named_by_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=content_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.NAMED_BY_STEREOTYPE.ea_guid)

    character_string_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=content_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=BclearerMatchedEaObjects.CHARACTER_STRINGS.ea_guid)

    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    output_universe_ea_classifiers = \
        output_universe.nf_ea_com_registry.get_ea_classifiers()

    output_universe_ea_packages = \
        output_universe.nf_ea_com_registry.get_ea_packages()

    for name_attribute_tuple in output_universe_name_attributes.itertuples():
        __convert_name_attribute_into_name_object(
            output_universe=output_universe,
            output_universe_ea_classifiers=output_universe_ea_classifiers,
            output_universe_ea_packages=output_universe_ea_packages,
            name_attribute_tuple=name_attribute_tuple,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            named_by_stereotype_nf_uuid=named_by_stereotype_nf_uuid,
            character_string_nf_uuid=character_string_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=output_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)

    log_message(
        message='CONVENTION SHIFT OPERATION: Extract attribute names to name objects - finished')

    return \
        output_universe


def __update_collection_with_dictionary(
        output_universe: NfEaComUniverses,
        dictionary: dict,
        collection_type: NfEaComCollectionTypes) \
        -> None:
    new_collection = \
        DataFrame.from_dict(
            data=dictionary,
            orient='index')

    output_universe.nf_ea_com_registry.update(
        collection_type=collection_type,
        new_collection=new_collection)


def __convert_name_attribute_into_name_object(
        output_universe: NfEaComUniverses,
        output_universe_ea_classifiers: DataFrame,
        output_universe_ea_packages: DataFrame,
        name_attribute_tuple: tuple,
        new_ea_objects_dictionary: dict,
        named_by_stereotype_nf_uuid: str,
        character_string_nf_uuid: str):
    attributed_object_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=name_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name)

    attributed_object_package_nf_uuid = \
        output_universe_ea_classifiers[
            output_universe_ea_classifiers[
                NfColumnTypes.NF_UUIDS.column_name] == attributed_object_nf_uuid][
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name].values[0]

    name_type_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=name_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name)

    name_attribute_name = \
        get_tuple_attribute_value_if_required(
            owning_tuple=name_attribute_tuple,
            attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name)

    name_attribute_type = \
        get_tuple_attribute_value_if_required(
            owning_tuple=name_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name)

    name_object_name = \
        name_attribute_name + ' ' + name_attribute_type[:-1]

    name_object_nf_uuid = \
        __create_name_object(
            output_universe_ea_packages=output_universe_ea_packages,
            new_ea_packages_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_PACKAGES],
            new_ea_classifiers_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS],
            package_nf_uuid=attributed_object_package_nf_uuid,
            name_object_name=name_object_name)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_object_nf_uuid,
        place_2_nf_uuid=name_type_nf_uuid,
        connector_type=EaConnectorTypes.DEPENDENCY)

    name_to_attributed_object_association_nf_uuid = \
        add_new_connector_to_dictionary(
            new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
            place_1_nf_uuid=name_object_nf_uuid,
            place_2_nf_uuid=attributed_object_nf_uuid,
            connector_type=EaConnectorTypes.ASSOCIATION)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=name_to_attributed_object_association_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
        stereotype_nf_uuid=named_by_stereotype_nf_uuid)

    name_attribute_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=name_attribute_tuple,
            attribute_name=NfColumnTypes.NF_UUIDS.column_name)

    __remove_attribute(
        nf_ea_com_universe=output_universe,
        attribute_nf_uuid=name_attribute_nf_uuid)

    add_new_attribute_to_dictionary(
        new_ea_attributes_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_ATTRIBUTES],
        name_object_nf_uuid=name_object_nf_uuid,
        attribute_value=name_attribute_name,
        attribute_name=NAME_INSTANCE_ATTRIBUTE_NAME,
        attribute_type_nf_uuid=character_string_nf_uuid)


def __create_name_object(
        output_universe_ea_packages: DataFrame,
        new_ea_packages_dictionary: dict,
        new_ea_classifiers_dictionary: dict,
        package_nf_uuid: str,
        name_object_name: str) \
        -> str:
    names_subpackage_nf_uuid = \
        create_new_subpackage_if_not_exist(
            nf_ea_com_universe_ea_packages=output_universe_ea_packages,
            new_ea_packages_dictionary=new_ea_packages_dictionary,
            package_nf_uuid=package_nf_uuid,
            new_subpackage_name='Names')

    name_object_nf_uuid = \
        add_new_class_to_dictionary(
            new_classifier_dictionary=new_ea_classifiers_dictionary,
            package_nf_uuid=names_subpackage_nf_uuid,
            class_name=name_object_name)

    return \
        name_object_nf_uuid


def __remove_attribute(
        nf_ea_com_universe: NfEaComUniverses,
        attribute_nf_uuid: str):
    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    updated_ea_attributes = \
        ea_attributes[
            ea_attributes[
                NfColumnTypes.NF_UUIDS.column_name] != attribute_nf_uuid]

    nf_ea_com_universe.nf_ea_com_registry.replace_collection(
        collection_type=NfEaComCollectionTypes.EA_ATTRIBUTES,
        collection=updated_ea_attributes)
