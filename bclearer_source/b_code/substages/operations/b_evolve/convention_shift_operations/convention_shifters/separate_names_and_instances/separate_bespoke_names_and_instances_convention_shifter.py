from bclearer_source.b_code.configurations.bespoke_name_to_instance_configuration_objects import BespokeNameToInstanceConfigurationObjects
from bclearer_source.b_code.substages.operations.b_evolve.common.new_root_package_creator import create_root_package
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.names_and_instances_annotator import annotate_names_and_instances
from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.separate_names_and_instances.names_and_instances_separator import separate_names_and_instances
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def shift_convention_separate_bespoke_names_and_instances(
        content_universe: NfEaComUniverses,
        list_of_configuration_objects: list,
        output_universe: NfEaComUniverses,
        package_name: str) \
        -> NfEaComUniverses:
    log_message(
        message='Separate Bespoke Names and Instances - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    for configuration_object in list_of_configuration_objects:
        __separate_names(
            configuration_object=configuration_object,
            nf_ea_com_universe=output_universe,
            package_name=package_name)

    log_message(
        message='Separate Bespoke Names and Instances - finished')

    return \
        output_universe


def __separate_names(
        configuration_object: BespokeNameToInstanceConfigurationObjects,
        nf_ea_com_universe: NfEaComUniverses,
        package_name: str):
    package_nf_uuid = \
        create_root_package(
            nf_ea_com_universe=nf_ea_com_universe,
            package_name=package_name)

    if configuration_object.matched_name_instance_type is None:
        separate_names_and_instances(
            nf_ea_com_universe=nf_ea_com_universe,
            matched_naming_space_type=configuration_object.matched_naming_space_type,
            name_instance_attribute_name=configuration_object.name_instance_attribute_name,
            package_nf_uuid=package_nf_uuid)

    else:
        annotate_names_and_instances(
            nf_ea_com_universe=nf_ea_com_universe,
            matched_name_instance_type=configuration_object.matched_name_instance_type)
