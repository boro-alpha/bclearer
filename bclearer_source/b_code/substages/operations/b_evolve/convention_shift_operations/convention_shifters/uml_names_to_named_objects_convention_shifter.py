from bclearer_source.b_code.configurations.uml_name_to_named_object_configuration_objects import UmlNameToNamedObjectConfigurationObjects
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.common.all_classifiers_of_a_package_and_its_subpackages_getter import get_all_package_and_subpackages_classifiers
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.common.has_classifier_ea_guid_attribute_type_name_and_value_checker import has_classifier_ea_guid_attribute_type_name_and_value
from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.constants.standard_constants import DEFAULT_NULL_VALUE
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def shift_convention_uml_names_to_named_objects(
        content_universe: NfEaComUniverses,
        list_of_configuration_objects: list,
        output_universe: NfEaComUniverses) \
        -> NfEaComUniverses:
    log_message(
        message='CONVENTION SHIFT OPERATION: Extract UML names to attributes - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    for configuration_object in list_of_configuration_objects:
        __shift_object_uml_name_to_named_object(
            configuration_object=configuration_object,
            output_universe=output_universe)

    log_message(
        message='CONVENTION SHIFT OPERATION: Extract UML names to attributes - finished')

    return \
        output_universe


def __shift_object_uml_name_to_named_object(
        configuration_object: UmlNameToNamedObjectConfigurationObjects,
        output_universe: NfEaComUniverses):
    package_guid = \
        configuration_object.matched_package.ea_guid

    naming_space_guid = \
        configuration_object.matched_naming_space.ea_guid

    # Only classes. Notes and boundaries (for example) are left out
    table_of_all_classifiers_of_a_package_and_its_subpackages = \
        get_all_package_and_subpackages_classifiers(
            content_universe=output_universe,
            package_ea_guid=package_guid)

    for index, domain_object_row in table_of_all_classifiers_of_a_package_and_its_subpackages.iterrows():
        name_string = \
            domain_object_row[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name]

        naming_space = \
            configuration_object.matched_naming_space.object_name

        classifier_ea_guid = \
            domain_object_row[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name]

        if not has_classifier_ea_guid_attribute_type_name_and_value(
                content_universe=output_universe,
                classifier_ea_guid=classifier_ea_guid,
                attribute_type_name=naming_space,
                attribute_value=name_string):
            __add_attribute_value_with_naming_space_type_to_output_universe(
                output_universe=output_universe,
                classifier_ea_guid=classifier_ea_guid,
                attribute_value=name_string,
                naming_space_ea_guid=naming_space_guid,
                naming_space=naming_space)


def __add_attribute_value_with_naming_space_type_to_output_universe(
        output_universe: NfEaComUniverses,
        classifier_ea_guid: str,
        attribute_value: str,
        naming_space_ea_guid: str,
        naming_space: str):
    output_universe_ea_attributes = \
        output_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_ATTRIBUTES]

    output_universe_ea_classifiers = \
        output_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_CLASSIFIERS]

    ea_guid_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name

    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    classifier_nf_uuid = \
        output_universe_ea_classifiers[
            output_universe_ea_classifiers[ea_guid_column_name] == classifier_ea_guid][
            nf_uuids_column_name].to_string(index=False).strip()

    naming_space_nf_uuid = \
        output_universe_ea_classifiers[
            output_universe_ea_classifiers[ea_guid_column_name] == naming_space_ea_guid][
            nf_uuids_column_name].to_string(index=False).strip()

    new_attribute_nf_uuid = \
        create_new_uuid()

    new_attribute_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=new_attribute_nf_uuid)

    output_universe_ea_attributes = \
        output_universe_ea_attributes.append({
            NfColumnTypes.NF_UUIDS.column_name: new_attribute_nf_uuid,
            NfEaComColumnTypes.ATTRIBUTES_LOWER_BOUNDS.column_name: '1',
            NfEaComColumnTypes.ATTRIBUTES_UPPER_BOUNDS.column_name: '1',
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name: classifier_nf_uuid,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name: naming_space_nf_uuid,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name: 'Public',
            NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name: naming_space,
            NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
            NfEaComColumnTypes.REPOSITORIED_OBJECTS_EA_REPOSITORY.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: attribute_value,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: new_attribute_ea_guid},
            ignore_index=True)

    output_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_ATTRIBUTES] = \
        output_universe_ea_attributes
