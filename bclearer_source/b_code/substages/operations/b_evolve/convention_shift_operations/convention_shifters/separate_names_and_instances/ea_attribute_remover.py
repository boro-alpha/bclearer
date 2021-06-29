from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def remove_ea_attributes(
        nf_ea_com_universe: NfEaComUniverses,
        ea_attributes: DataFrame):
    ea_attribute_nf_uuids_to_remove = \
        set(
            ea_attributes[NfColumnTypes.NF_UUIDS.column_name])

    ea_attributes = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()

    remaining_ea_attributes = \
        ea_attributes[~ea_attributes[NfColumnTypes.NF_UUIDS.column_name].isin(ea_attribute_nf_uuids_to_remove)]

    nf_ea_com_universe.nf_ea_com_registry.replace_collection(
        collection_type=NfEaComCollectionTypes.EA_ATTRIBUTES,
        collection=remaining_ea_attributes)
