from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import \
    NfEaComColumnTypes
from pandas import DataFrame

from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def get_digitalisation_level_stereotypes_usages(
        nf_ea_com_universe: NfEaComUniverses) \
        -> DataFrame:
    digitalisation_level_stereotype_ea_guids = \
        DigitalisationLevelStereotypeMatchedEaObjects.get_ea_guids()

    ea_stereotypes =  \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()

    digitalisation_level_stereotypes = \
        ea_stereotypes[ea_stereotypes[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name].isin(digitalisation_level_stereotype_ea_guids)]

    digitalisation_level_stereotypes_nf_uuids = \
        set(
            digitalisation_level_stereotypes[NfColumnTypes.NF_UUIDS.column_name])

    ea_stereotype_usages = \
        nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.STEREOTYPE_USAGE]

    digitalisation_level_stereotypes_usages = \
        ea_stereotype_usages[ea_stereotype_usages['stereotype_nf_uuids'].isin(digitalisation_level_stereotypes_nf_uuids)]

    return \
        digitalisation_level_stereotypes_usages
