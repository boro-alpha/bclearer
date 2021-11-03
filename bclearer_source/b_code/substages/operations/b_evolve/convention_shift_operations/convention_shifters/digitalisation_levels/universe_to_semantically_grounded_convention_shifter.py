from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses

from bclearer_source.b_code.substages.operations.a_load.content_operations.digitalisation_levels.digitalisation_level_stereotype_replacer import \
    replace_digitalisation_level_stereotype


def shift_convention_universe_to_semantically_grounded(
        content_universe: NfEaComUniverses,
        output_universe: NfEaComUniverses) \
        -> NfEaComUniverses:
    log_message(
        message='Shift Universe to Semantically Grounded Digitalisation Level - started')

    output_universe.nf_ea_com_registry.dictionary_of_collections = \
        content_universe.nf_ea_com_registry.dictionary_of_collections.copy()

    replace_digitalisation_level_stereotype(
        nf_ea_com_universe=output_universe,
        digitalisation_level_stereotype=DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE)

    log_message(
        message='Shift Universe to Semantically Grounded Digitalisation Level - finished')

    return \
        output_universe
