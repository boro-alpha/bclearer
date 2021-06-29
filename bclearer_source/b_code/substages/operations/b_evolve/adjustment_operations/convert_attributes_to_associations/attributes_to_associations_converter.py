from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.attributes_converter import convert_attributes
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.convert_attributes_to_associations.attributes_to_convert_getter import get_attributes_to_convert
from bclearer_source.b_code.substages.operations.b_evolve.adjustment_operations.remove_attributes.attribute_remover import remove_attributes
from bclearer_source.b_code.substages.operations.b_evolve.common.new_root_package_creator import create_root_package
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_association_direction_types import EaAssociationDirectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def convert_attributes_to_associations(
        content_universe: NfEaComUniverses,
        adjustment_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        direction: EaAssociationDirectionTypes,
        package_name: str) \
        -> None:
    __run_input_checks()

    __run_operation(
        content_universe=content_universe,
        adjustment_universe=adjustment_universe,
        output_universe=output_universe,
        direction=direction,
        package_name=package_name)


def __run_input_checks():
    pass


def __run_operation(
        content_universe: NfEaComUniverses,
        adjustment_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses,
        direction: EaAssociationDirectionTypes,
        package_name: str):
    log_message(
        message='ADJUSTMENT OPERATION: Convert attributes - started')

    attributes_to_convert = \
        get_attributes_to_convert(
            content_universe=content_universe,
            adjustment_universe=adjustment_universe)

    package_nf_uuid = \
        create_root_package(
            nf_ea_com_universe=content_universe,
            package_name=package_name)

    __copy_collections(
            content_universe=content_universe,
            output_universe=output_universe)

    convert_attributes(
        output_universe=output_universe,
        attributes_to_convert=attributes_to_convert,
        direction=direction,
        package_nf_uuid=package_nf_uuid)

    log_message(
        message='ADJUSTMENT OPERATION: Convert attributes - removing converted attributes')

    remove_attributes(
        content_universe=output_universe,
        adjustment_universe=adjustment_universe,
        output_universe=output_universe)

    log_message(
        message='ADJUSTMENT OPERATION: Convert attributes - finished')


def __copy_collections(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> None:
    content_collections_dictionary = \
        content_universe.nf_ea_com_registry.dictionary_of_collections

    output_collections_dictionary = \
        output_universe.nf_ea_com_registry.dictionary_of_collections

    for content_collection_type, content_collection_table in content_collections_dictionary.items():
        output_collections_dictionary[content_collection_type] = \
            content_collection_table
