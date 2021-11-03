from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from bclearer_source.b_code.common_knowledge.bclearer_additional_column_types import BclearerAdditionalColumnTypes
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.ea_attribute_remover import remove_ea_attributes
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.name_instance_creator import create_name_instance
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.name_instance_type_creator import create_name_instance_type
from bclearer_source.b_code.substages.operations.common.instances_nf_uuids_getter import get_instances_nf_uuids_of_matched_type
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from nf_common_source.code.constants.standard_constants import DEFAULT_FOREIGN_TABLE_SUFFIX, DEFAULT_MASTER_TABLE_SUFFIX
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.dataframe_service.dataframe_mergers import left_merge_dataframes
from nf_common_source.code.services.reporting_service.wrappers.run_and_log_function_wrapper import run_and_log_function
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


@run_and_log_function
def separate_names_and_instances(
        nf_ea_com_universe: NfEaComUniverses,
        matched_naming_space_type: MatchedEaObjects,
        name_instance_attribute_name: str,
        package_nf_uuid: str):
    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_dependencies = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    naming_space_instances = \
        get_instances_nf_uuids_of_matched_type(
            nf_ea_com_universe=nf_ea_com_universe,
            matched_type=matched_naming_space_type)

    __remove_attribute_from_type(
        nf_ea_com_universe=nf_ea_com_universe,
        matched_naming_space_type=matched_naming_space_type,
        name_instance_attribute_name=name_instance_attribute_name)

    digitalisation_level_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE.ea_guid)

    for naming_space_instance_nf_uuid in naming_space_instances:
        __separate_name_instances(
            nf_ea_com_universe=nf_ea_com_universe,
            ea_dependencies=ea_dependencies,
            naming_space_instance_nf_uuid=naming_space_instance_nf_uuid,
            name_instance_attribute_name=name_instance_attribute_name,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


@run_and_log_function
def __separate_name_instances(
        nf_ea_com_universe: NfEaComUniverses,
        ea_dependencies: DataFrame,
        naming_space_instance_nf_uuid: str,
        name_instance_attribute_name: str,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str,
        digitalisation_level_stereotype_nf_uuid: str):
    name_instance_type_nf_uuid = \
        create_name_instance_type(
            nf_ea_com_universe=nf_ea_com_universe,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            name_object_name=name_instance_attribute_name,
            naming_space_nf_uuid=naming_space_instance_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    name_types_instances_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE.ea_guid)

    name_instance_attributes = \
        __get_name_instance_attributes(
            nf_ea_com_universe=nf_ea_com_universe,
            ea_dependencies=ea_dependencies,
            naming_space_instance_nf_uuid=naming_space_instance_nf_uuid,
            name_instance_attribute_name=name_instance_attribute_name)

    for ea_attribute_tuple in name_instance_attributes.itertuples():
        create_name_instance(
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            ea_attribute_tuple=ea_attribute_tuple,
            name_instance_type_nf_uuid=name_instance_type_nf_uuid,
            name_types_instances_stereotype_nf_uuid=name_types_instances_stereotype_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    remove_ea_attributes(
        nf_ea_com_universe=nf_ea_com_universe,
        ea_attributes=name_instance_attributes)


@run_and_log_function
def __get_name_instance_attributes(
        nf_ea_com_universe: NfEaComUniverses,
        ea_dependencies: DataFrame,
        naming_space_instance_nf_uuid: str,
        name_instance_attribute_name: str) \
        -> DataFrame:
    filtered_dependencies = \
        ea_dependencies[ea_dependencies[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name] == naming_space_instance_nf_uuid]

    name_instances = \
        set(filtered_dependencies[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name])

    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    name_instance_attributes = \
        ea_attributes.loc[ea_attributes[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name].isin(name_instances)]

    filtered_name_instance_attributes = \
        name_instance_attributes[name_instance_attributes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] == name_instance_attribute_name]

    ea_classifiers = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    extended_filtered_name_instance_attributes = \
        left_merge_dataframes(
            master_dataframe=filtered_name_instance_attributes,
            master_dataframe_key_columns=[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name],
            merge_suffixes=[DEFAULT_FOREIGN_TABLE_SUFFIX, DEFAULT_MASTER_TABLE_SUFFIX],
            foreign_key_dataframe=ea_classifiers,
            foreign_key_dataframe_fk_columns=[NfColumnTypes.NF_UUIDS.column_name],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: BclearerAdditionalColumnTypes.OWNING_OBJECT_NAMES.column_name})

    return \
        extended_filtered_name_instance_attributes


def __remove_attribute_from_type(
        nf_ea_com_universe: NfEaComUniverses,
        matched_naming_space_type: MatchedEaObjects,
        name_instance_attribute_name: str):
    naming_space_type_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=matched_naming_space_type.ea_guid)

    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    naming_space_type_attributes = \
        ea_attributes.loc[ea_attributes[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name] == naming_space_type_nf_uuid]

    filtered_naming_space_type_attributes = \
        naming_space_type_attributes[naming_space_type_attributes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] == name_instance_attribute_name]

    remove_ea_attributes(
        nf_ea_com_universe=nf_ea_com_universe,
        ea_attributes=filtered_naming_space_type_attributes)
