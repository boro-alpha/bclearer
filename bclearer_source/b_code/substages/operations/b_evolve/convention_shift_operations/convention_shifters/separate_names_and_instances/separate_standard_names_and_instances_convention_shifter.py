from bclearer_source.b_code.common_knowledge.bclearer_matched_ea_objects import BclearerMatchedEaObjects
from bclearer_source.b_code.common_knowledge.bclearer_additional_column_types import BclearerAdditionalColumnTypes
from bclearer_source.b_code.common_knowledge.bclearer_constants import NAME_INSTANCE_ATTRIBUTE_NAME
from bclearer_source.b_code.substages.operations.b_evolve.common.new_root_package_creator import create_root_package
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.ea_attribute_remover import remove_ea_attributes
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.name_instance_creator import create_name_instance
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.name_instance_type_creator import create_name_instance_type
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from nf_common_source.code.constants.standard_constants import DEFAULT_FOREIGN_TABLE_SUFFIX
from nf_common_source.code.constants.standard_constants import DEFAULT_MASTER_TABLE_SUFFIX
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.dataframe_service.dataframe_mergers import left_merge_dataframes
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def shift_convention_separate_standard_names_and_instances(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        package_name: str) \
        -> NfEaComUniverses:
    log_message(
        message='Separate Standard Names and Instances - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    __separate_names_and_instances(
        nf_ea_com_universe=output_universe,
        package_name=package_name)

    log_message(
        message='Separate Standard Names and Instances - finished')

    return \
        output_universe


def __separate_names_and_instances(
        nf_ea_com_universe: NfEaComUniverses,
        package_name: str):
    package_nf_uuid = \
        create_root_package(
            nf_ea_com_universe=nf_ea_com_universe,
            package_name=package_name)

    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    attributes_grouped_by_naming_space_dictionary = \
        __get_attributes_grouped_by_naming_space_dictionary(
            nf_ea_com_universe=nf_ea_com_universe)

    for naming_space_nf_uuid, attributes in attributes_grouped_by_naming_space_dictionary.items():
        __separate_naming_space_instances(
            nf_ea_com_universe=nf_ea_com_universe,
            naming_space_nf_uuid=naming_space_nf_uuid,
            ea_attributes=attributes,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __separate_naming_space_instances(
        nf_ea_com_universe: NfEaComUniverses,
        naming_space_nf_uuid: str,
        ea_attributes: DataFrame,
        new_ea_objects_dictionary: dict,
        package_nf_uuid: str):
    ea_classifiers = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    naming_space_name = \
        ea_classifiers.at[ea_classifiers[NfColumnTypes.NF_UUIDS.column_name].eq(
            naming_space_nf_uuid).idxmax(), NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name]

    name_instance_type_name = \
        naming_space_name[:-1] + ' Instances'

    name_instance_type_nf_uuid = \
        create_name_instance_type(
            nf_ea_com_universe=nf_ea_com_universe,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            name_object_name=name_instance_type_name,
            naming_space_nf_uuid=naming_space_nf_uuid)

    name_types_instances_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE.ea_guid)

    for ea_attribute_tuple in ea_attributes.itertuples():
        create_name_instance(
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            ea_attribute_tuple=ea_attribute_tuple,
            name_instance_type_nf_uuid=name_instance_type_nf_uuid,
            name_types_instances_stereotype_nf_uuid=name_types_instances_stereotype_nf_uuid)

    remove_ea_attributes(
        nf_ea_com_universe=nf_ea_com_universe,
        ea_attributes=ea_attributes)


def __get_attributes_grouped_by_naming_space_dictionary(
        nf_ea_com_universe: NfEaComUniverses) \
        -> dict:
    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    standard_name_instance_attributes = \
        ea_attributes[ea_attributes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] == NAME_INSTANCE_ATTRIBUTE_NAME]

    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_dependencies = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    extended_standard_name_instance_attributes = \
        left_merge_dataframes(
            master_dataframe=standard_name_instance_attributes,
            master_dataframe_key_columns=[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name],
            merge_suffixes=[DEFAULT_FOREIGN_TABLE_SUFFIX, DEFAULT_MASTER_TABLE_SUFFIX],
            foreign_key_dataframe=ea_dependencies,
            foreign_key_dataframe_fk_columns=[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: BclearerAdditionalColumnTypes.NAMING_SPACE_NF_UUIDS.column_name})

    ea_classifiers = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()

    extended_standard_name_instance_attributes = \
        left_merge_dataframes(
            master_dataframe=extended_standard_name_instance_attributes,
            master_dataframe_key_columns=[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name],
            merge_suffixes=[DEFAULT_FOREIGN_TABLE_SUFFIX, DEFAULT_MASTER_TABLE_SUFFIX],
            foreign_key_dataframe=ea_classifiers,
            foreign_key_dataframe_fk_columns=[NfColumnTypes.NF_UUIDS.column_name],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: BclearerAdditionalColumnTypes.OWNING_OBJECT_NAMES.column_name})

    naming_space_nf_uuids = \
        set(extended_standard_name_instance_attributes[BclearerAdditionalColumnTypes.NAMING_SPACE_NF_UUIDS.column_name])

    attributes_grouped_by_name_space_dictionary = {}

    for naming_space_nf_uuid in naming_space_nf_uuids:
        naming_space_ea_attributes = \
            extended_standard_name_instance_attributes[extended_standard_name_instance_attributes[BclearerAdditionalColumnTypes.NAMING_SPACE_NF_UUIDS.column_name] == naming_space_nf_uuid]

        attributes_grouped_by_name_space_dictionary[naming_space_nf_uuid] = \
            naming_space_ea_attributes

    return \
        attributes_grouped_by_name_space_dictionary
