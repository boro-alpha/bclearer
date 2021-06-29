from bclearer_source.b_code.configurations.generalise_names_configuration_objects import GeneraliseNamesConfigurationObjects
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.generalise_names.stereotype_instances_associations_adder import add_stereotype_to_instances_associations
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.connector_rename import rename_connector
from bclearer_source.b_code.substages.operations.common.intersection_getter import get_intersection_of_dependency_and_association_linked
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def shift_convention_generalise_names(
        content_universe: NfEaComUniverses,
        list_of_configuration_objects: list,
        output_universe: NfEaComUniverses) \
        -> NfEaComUniverses:
    log_message(
        message='Generalise Names - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    __generalise_naming_spaces(
        list_of_configuration_objects=list_of_configuration_objects,
        nf_ea_com_universe=output_universe)

    log_message(
        message='Generalise Names - finished')

    return \
        output_universe


def __generalise_naming_spaces(
        list_of_configuration_objects: list,
        nf_ea_com_universe: NfEaComUniverses):
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    for configuration_object in list_of_configuration_objects:
        __generalise_naming_space(
            configuration_object=configuration_object,
            nf_ea_com_universe=nf_ea_com_universe,
            new_ea_objects_dictionary=new_ea_objects_dictionary)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __generalise_naming_space(
        configuration_object: GeneraliseNamesConfigurationObjects,
        nf_ea_com_universe: NfEaComUniverses,
        new_ea_objects_dictionary: dict):
    naming_space_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=configuration_object.matched_naming_space.ea_guid)

    named_object_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=configuration_object.matched_named_object.ea_guid)

    name_subtype_nf_uuid = \
        get_intersection_of_dependency_and_association_linked(
            nf_ea_com_universe=nf_ea_com_universe,
            linked_by_dependency_nf_uuid=naming_space_nf_uuid,
            linked_by_association_nf_uuid=named_object_nf_uuid)

    __add_generalisation(
        configuration_object=configuration_object,
        output_universe=nf_ea_com_universe,
        name_subtype_nf_uuid=name_subtype_nf_uuid,
        new_ea_objects_dictionary=new_ea_objects_dictionary)

    __add_association_name(
        configuration_object=configuration_object,
        output_universe=nf_ea_com_universe,
        named_object_nf_uuid=named_object_nf_uuid,
        name_subtype_nf_uuid=name_subtype_nf_uuid)

    __add_stereotype(
        configuration_object=configuration_object,
        output_universe=nf_ea_com_universe,
        name_subtype_nf_uuid=name_subtype_nf_uuid)


def __add_generalisation(
        configuration_object: GeneraliseNamesConfigurationObjects,
        output_universe: NfEaComUniverses,
        name_subtype_nf_uuid: str,
        new_ea_objects_dictionary: dict):
    name_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=output_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=configuration_object.matched_name.ea_guid)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_subtype_nf_uuid,
        place_2_nf_uuid=name_nf_uuid,
        connector_type=EaConnectorTypes.GENERALIZATION)


def __add_association_name(
        configuration_object: GeneraliseNamesConfigurationObjects,
        output_universe: NfEaComUniverses,
        named_object_nf_uuid: str,
        name_subtype_nf_uuid: str):
    rename_connector(
        nf_ea_com_universe=output_universe,
        place_1_nf_uuid=name_subtype_nf_uuid,
        place_2_nf_uuid=named_object_nf_uuid,
        connector_type=EaConnectorTypes.ASSOCIATION,
        connector_name=configuration_object.matched_named_by_stereotype.object_name)


def __add_stereotype(
        configuration_object: GeneraliseNamesConfigurationObjects,
        output_universe: NfEaComUniverses,
        name_subtype_nf_uuid: str):
    named_by_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=output_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=configuration_object.matched_named_by_stereotype.ea_guid)

    add_stereotype_to_instances_associations(
        nf_ea_com_universe=output_universe,
        type_nf_uuid=name_subtype_nf_uuid,
        stereotype_nf_uuid=named_by_stereotype_nf_uuid)
