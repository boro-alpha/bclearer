from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.instances_nf_uuids_getter import get_instances_nf_uuids_of_matched_type
from bclearer_source.b_code.substages.operations.common.instances_nf_uuids_getter import get_instances_nf_uuids_of_type_nf_uuid
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.reporting_service.wrappers.run_and_log_function_wrapper import run_and_log_function
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


@run_and_log_function
def annotate_names_and_instances(
        nf_ea_com_universe: NfEaComUniverses,
        matched_name_instance_type: MatchedEaObjects):
    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    name_instance_instances = \
        get_instances_nf_uuids_of_matched_type(
            nf_ea_com_universe=nf_ea_com_universe,
            matched_type=matched_name_instance_type)

    for name_instance_instance_nf_uuid in name_instance_instances:
        __annotate_naming_space_instances(
            nf_ea_com_universe=nf_ea_com_universe,
            name_instance_instance_nf_uuid=name_instance_instance_nf_uuid,
            new_ea_objects_dictionary=new_ea_objects_dictionary)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


@run_and_log_function
def __annotate_naming_space_instances(
        nf_ea_com_universe: NfEaComUniverses,
        name_instance_instance_nf_uuid: str,
        new_ea_objects_dictionary: dict):
    name_instances_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=BclearerMatchedEaObjects.NAME_INSTANCES.ea_guid)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_instance_instance_nf_uuid,
        place_2_nf_uuid=name_instances_nf_uuid,
        connector_type=EaConnectorTypes.GENERALIZATION)

    __add_stereotype_usages(
        nf_ea_com_universe=nf_ea_com_universe,
        name_instance_instance_nf_uuid=name_instance_instance_nf_uuid,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __add_stereotype_usages(
        nf_ea_com_universe: NfEaComUniverses,
        name_instance_instance_nf_uuid: str,
        new_ea_objects_dictionary: dict):
    name_instance_instances = \
        get_instances_nf_uuids_of_type_nf_uuid(
            nf_ea_com_universe=nf_ea_com_universe,
            nf_uuid=name_instance_instance_nf_uuid)

    name_types_instances_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE.ea_guid)

    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_associations = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.ASSOCIATION.type_name]

    filtered_associations = \
        ea_associations[ea_associations[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name].isin(name_instance_instances)]

    association_nf_uuids = \
        set(filtered_associations[NfColumnTypes.NF_UUIDS.column_name])

    for association_nf_uuid in association_nf_uuids:
        add_new_stereotype_usage_to_dictionary(
            new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
            client_nf_uuid=association_nf_uuid,
            client_collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
            stereotype_nf_uuid=name_types_instances_stereotype_nf_uuid)
