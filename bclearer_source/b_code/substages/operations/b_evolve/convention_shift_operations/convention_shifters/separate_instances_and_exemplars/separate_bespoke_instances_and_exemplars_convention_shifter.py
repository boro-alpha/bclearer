from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes

from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.configurations.bespoke_instance_to_exemplar_configuration_objects import BespokeInstanceToExemplarConfigurationObjects
from bclearer_source.b_code.substages.operations.b_evolve.common.new_root_package_creator import create_root_package
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_instances_and_exemplars.instances_and_exemplars_separator import separate_instances_and_exemplars
from bclearer_source.b_code.substages.operations.common.instances_nf_uuids_getter import get_instances_nf_uuids_of_matched_type
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame

from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection


def shift_convention_separate_bespoke_instances_and_exemplars(
        content_universe: NfEaComUniverses,
        list_of_configuration_objects: list,
        output_universe: NfEaComUniverses,
        package_name: str) \
        -> NfEaComUniverses:
    log_message(
        message='Separate Bespoke Instances and Exemplars - started')

    package_nf_uuid = \
        create_root_package(
            nf_ea_com_universe=content_universe,
            package_name=package_name)

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    for configuration_object in list_of_configuration_objects:
        __separate_instances_and_exemplars(
            configuration_object=configuration_object,
            nf_ea_com_universe=output_universe,
            package_nf_uuid=package_nf_uuid)

    log_message(
        message='Separate Bespoke Instances and Exemplars - finished')

    return \
        output_universe


def __separate_instances_and_exemplars(
        configuration_object: BespokeInstanceToExemplarConfigurationObjects,
        nf_ea_com_universe: NfEaComUniverses,
        package_nf_uuid: str):
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    name_instance_instances = \
        get_instances_nf_uuids_of_matched_type(
            nf_ea_com_universe=nf_ea_com_universe,
            matched_type=configuration_object.matched_name_instance_instance)

    digitalisation_level_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE.ea_guid)

    for name_instance_instance_nf_uuid in name_instance_instances:
        __separate_name_exemplars(
            nf_ea_com_universe=nf_ea_com_universe,
            name_instance_instance_nf_uuid=name_instance_instance_nf_uuid,
            name_exemplar_attribute_name=configuration_object.name_exemplar_attribute_name,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __separate_name_exemplars(
        nf_ea_com_universe: NfEaComUniverses,
        name_instance_instance_nf_uuid: str,
        name_exemplar_attribute_name: str,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        digitalisation_level_stereotype_nf_uuid: str):
    ea_attributes = \
        __get_name_exemplar_attributes(
            nf_ea_com_universe=nf_ea_com_universe,
            name_instance_instance_nf_uuid=name_instance_instance_nf_uuid,
            name_exemplar_attribute_name=name_exemplar_attribute_name)

    separate_instances_and_exemplars(
        nf_ea_com_universe=nf_ea_com_universe,
        name_instance_type_nf_uuid=name_instance_instance_nf_uuid,
        ea_attributes=ea_attributes,
        new_ea_objects_dictionary=new_ea_objects_dictionary,
        package_nf_uuid=package_nf_uuid,
        digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)


def __get_name_exemplar_attributes(
        nf_ea_com_universe: NfEaComUniverses,
        name_instance_instance_nf_uuid: str,
        name_exemplar_attribute_name: str) \
        -> DataFrame:
    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_dependencies = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    filtered_dependencies = \
        ea_dependencies[ea_dependencies[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name] == name_instance_instance_nf_uuid]

    name_instances = \
        set(filtered_dependencies[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name])

    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    name_instance_attributes = \
        ea_attributes.loc[ea_attributes[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name].isin(name_instances)]

    filtered_name_instance_attributes = \
        name_instance_attributes[name_instance_attributes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] == name_exemplar_attribute_name]

    return \
        filtered_name_instance_attributes
