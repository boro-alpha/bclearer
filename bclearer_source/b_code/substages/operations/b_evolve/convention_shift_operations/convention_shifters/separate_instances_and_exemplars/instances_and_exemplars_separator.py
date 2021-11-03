from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.ea_attribute_remover import remove_ea_attributes
from bclearer_source.b_code.substages.operations.common.class_adder import add_new_class_to_dictionary
from bclearer_source.b_code.substages.operations.common.connector_adder import add_new_connector_to_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from bclearer_source.b_code.substages.operations.common.stereotype_adder import add_new_stereotype_usage_to_dictionary
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.tuple_service.tuple_attribute_value_getter import get_tuple_attribute_value_if_required
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def separate_instances_and_exemplars(
        nf_ea_com_universe: NfEaComUniverses,
        name_instance_type_nf_uuid: str,
        ea_attributes: DataFrame,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        digitalisation_level_stereotype_nf_uuid: str):
    ea_classifiers = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    name_instance_type_name = \
        ea_classifiers.at[ea_classifiers[NfColumnTypes.NF_UUIDS.column_name].eq(
            name_instance_type_nf_uuid).idxmax(), NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name]

    if 'Instances' in name_instance_type_name:
        name_exemplar_type_name = \
            name_instance_type_name.replace(
                'Instances',
                'Exemplars')

    else:
        name_exemplar_type_name = \
            name_instance_type_name + ' Exemplars'

    name_exemplar_type_nf_uuid = \
        __create_name_exemplar_type(
            nf_ea_com_universe=nf_ea_com_universe,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            name_exemplar_type_name=name_exemplar_type_name,
            name_instance_type_nf_uuid=name_instance_type_nf_uuid)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=name_exemplar_type_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
        stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    exemplified_by_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.EXEMPLIFIED_BY_STEREOTYPE.ea_guid)

    name_exemplar_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.NAME_EXEMPLAR_STEREOTYPE.ea_guid)

    for ea_attribute_tuple in ea_attributes.itertuples():
        __create_name_exemplar(
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            ea_attribute_tuple=ea_attribute_tuple,
            name_exemplar_type_nf_uuid=name_exemplar_type_nf_uuid,
            exemplified_by_stereotype_nf_uuid=exemplified_by_stereotype_nf_uuid,
            name_exemplar_stereotype_nf_uuid=name_exemplar_stereotype_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    remove_ea_attributes(
        nf_ea_com_universe=nf_ea_com_universe,
        ea_attributes=ea_attributes)


def __create_name_exemplar_type(
        nf_ea_com_universe: NfEaComUniverses,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        name_exemplar_type_name: str,
        name_instance_type_nf_uuid: str) \
        -> str:
    name_exemplar_type_nf_uuid = \
        add_new_class_to_dictionary(
            new_classifier_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS],
            package_nf_uuid=package_nf_uuid,
            class_name=name_exemplar_type_name)

    name_exemplars_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=BclearerMatchedEaObjects.NAME_EXEMPLARS.ea_guid)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_exemplar_type_nf_uuid,
        place_2_nf_uuid=name_exemplars_nf_uuid,
        connector_type=EaConnectorTypes.GENERALIZATION)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_exemplar_type_nf_uuid,
        place_2_nf_uuid=name_instance_type_nf_uuid,
        connector_type=EaConnectorTypes.ASSOCIATION,
        connector_name=BclearerMatchedEaObjects.EXEMPLIFIED_BY_STEREOTYPE.object_name)

    return \
        name_exemplar_type_nf_uuid


def __create_name_exemplar(
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        ea_attribute_tuple: tuple,
        name_exemplar_type_nf_uuid: str,
        exemplified_by_stereotype_nf_uuid: str,
        name_exemplar_stereotype_nf_uuid: str,
        digitalisation_level_stereotype_nf_uuid: str):
    attributed_object_nf_uuid = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name)

    name_exemplar_name = \
        get_tuple_attribute_value_if_required(
            owning_tuple=ea_attribute_tuple,
            attribute_name=NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name)

    name_exemplar_nf_uuid = \
        add_new_class_to_dictionary(
            new_classifier_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CLASSIFIERS],
            package_nf_uuid=package_nf_uuid,
            class_name=name_exemplar_name)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=name_exemplar_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
        stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
        place_1_nf_uuid=name_exemplar_nf_uuid,
        place_2_nf_uuid=name_exemplar_type_nf_uuid,
        connector_type=EaConnectorTypes.DEPENDENCY)

    association_nf_uuid = \
        add_new_connector_to_dictionary(
            new_connector_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.EA_CONNECTORS],
            place_1_nf_uuid=name_exemplar_nf_uuid,
            place_2_nf_uuid=attributed_object_nf_uuid,
            connector_type=EaConnectorTypes.ASSOCIATION)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=association_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
        stereotype_nf_uuid=exemplified_by_stereotype_nf_uuid)

    add_new_stereotype_usage_to_dictionary(
        new_stereotype_usage_dictionary=new_ea_objects_dictionary[NfEaComCollectionTypes.STEREOTYPE_USAGE],
        client_nf_uuid=name_exemplar_nf_uuid,
        client_collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
        stereotype_nf_uuid=name_exemplar_stereotype_nf_uuid)
