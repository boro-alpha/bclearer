from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import \
    NfEaComCollectionTypes

from bclearer_source.b_code.common_knowledge.bclearer_additional_column_types import BclearerAdditionalColumnTypes
from bclearer_source.b_code.common_knowledge.bclearer_constants import NAME_EXEMPLAR_ATTRIBUTE_NAME
from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.substages.operations.b_evolve.common.new_root_package_creator import create_root_package
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_instances_and_exemplars.instances_and_exemplars_separator import separate_instances_and_exemplars
from bclearer_source.b_code.substages.operations.common.new_ea_objects_dictionary_creator import create_new_ea_objects_dictionary
from bclearer_source.b_code.substages.operations.common.nf_ea_com_universe_updater import update_nf_ea_com_universe_with_dictionary
from nf_common_source.code.constants.standard_constants import DEFAULT_FOREIGN_TABLE_SUFFIX
from nf_common_source.code.constants.standard_constants import DEFAULT_MASTER_TABLE_SUFFIX
from nf_common_source.code.services.dataframe_service.dataframe_mergers import left_merge_dataframes
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses

from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import \
    get_nf_uuid_from_ea_guid_from_collection


def shift_convention_separate_standard_instances_and_exemplars(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        package_name: str) \
        -> NfEaComUniverses:
    log_message(
        message='Separate Standard Instances and Exemplars - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    __separate_instances_and_exemplars(
        nf_ea_com_universe=output_universe,
        package_name=package_name)

    log_message(
        message='Separate Standard Instances and Exemplars - finished')

    return \
        output_universe


def __separate_instances_and_exemplars(
        nf_ea_com_universe: NfEaComUniverses,
        package_name: str):
    package_nf_uuid = \
        create_root_package(
            nf_ea_com_universe=nf_ea_com_universe,
            package_name=package_name)

    new_ea_objects_dictionary = \
        create_new_ea_objects_dictionary()

    attributes_grouped_by_name_instance_type_dictionary = \
        __get_attributes_grouped_by_name_instance_type_dictionary(
            nf_ea_com_universe=nf_ea_com_universe)

    digitalisation_level_stereotype_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            ea_guid=DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE.ea_guid)

    for name_instance_type_nf_uuid, ea_attributes in attributes_grouped_by_name_instance_type_dictionary.items():
        separate_instances_and_exemplars(
            nf_ea_com_universe=nf_ea_com_universe,
            name_instance_type_nf_uuid=name_instance_type_nf_uuid,
            ea_attributes=ea_attributes,
            new_ea_objects_dictionary=new_ea_objects_dictionary,
            package_nf_uuid=package_nf_uuid,
            digitalisation_level_stereotype_nf_uuid=digitalisation_level_stereotype_nf_uuid)

    update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe=nf_ea_com_universe,
        new_ea_objects_dictionary=new_ea_objects_dictionary)


def __get_attributes_grouped_by_name_instance_type_dictionary(
        nf_ea_com_universe: NfEaComUniverses) \
        -> dict:
    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    standard_name_exemplar_attributes = \
        ea_attributes[ea_attributes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] == NAME_EXEMPLAR_ATTRIBUTE_NAME]

    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_dependencies = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    extended_standard_name_exemplar_attributes = \
        left_merge_dataframes(
            master_dataframe=standard_name_exemplar_attributes,
            master_dataframe_key_columns=[NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name],
            merge_suffixes=[DEFAULT_FOREIGN_TABLE_SUFFIX, DEFAULT_MASTER_TABLE_SUFFIX],
            foreign_key_dataframe=ea_dependencies,
            foreign_key_dataframe_fk_columns=[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name],
            foreign_key_dataframe_other_column_rename_dictionary={
                NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: BclearerAdditionalColumnTypes.NAME_INSTANCE_TYPE_NF_UUIDS.column_name})

    name_instance_type_nf_uuids = \
        set(extended_standard_name_exemplar_attributes[BclearerAdditionalColumnTypes.NAME_INSTANCE_TYPE_NF_UUIDS.column_name])

    attributes_grouped_by_name_instance_type_dictionary = \
        dict()

    for name_instance_type_nf_uuid in name_instance_type_nf_uuids:
        name_instance_type_ea_attributes = \
            extended_standard_name_exemplar_attributes[extended_standard_name_exemplar_attributes[BclearerAdditionalColumnTypes.NAME_INSTANCE_TYPE_NF_UUIDS.column_name] == name_instance_type_nf_uuid]

        attributes_grouped_by_name_instance_type_dictionary[name_instance_type_nf_uuid] = \
            name_instance_type_ea_attributes

    return \
        attributes_grouped_by_name_instance_type_dictionary
