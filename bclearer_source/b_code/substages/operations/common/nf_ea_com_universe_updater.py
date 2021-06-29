from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from pandas import DataFrame


def update_nf_ea_com_universe_with_dictionary(
        nf_ea_com_universe: NfEaComUniverses,
        new_ea_objects_dictionary: dict) \
        -> None:
    for collection_type, new_collection_as_dictionary in new_ea_objects_dictionary.items():
        __update_collection_if_required(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=collection_type,
            new_collection_as_dictionary=new_collection_as_dictionary)


def __update_collection_if_required(
        nf_ea_com_universe: NfEaComUniverses,
        collection_type: NfEaComCollectionTypes,
        new_collection_as_dictionary: dict):
    if len(new_collection_as_dictionary) == 0:
        return

    new_collection = \
        DataFrame.from_dict(
            data=new_collection_as_dictionary,
            orient='Index')

    nf_ea_com_universe.nf_ea_com_registry.update(
        collection_type=collection_type,
        new_collection=new_collection)
