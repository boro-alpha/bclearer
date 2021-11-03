from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes


def create_new_ea_objects_dictionary() \
        -> dict:
    new_ea_objects_dictionary = \
        {
            NfEaComCollectionTypes.EA_CLASSIFIERS: dict(),
            NfEaComCollectionTypes.EA_CONNECTORS: dict(),
            NfEaComCollectionTypes.EA_PACKAGES: dict(),
            NfEaComCollectionTypes.EA_ATTRIBUTES: dict(),
            NfEaComCollectionTypes.STEREOTYPE_USAGE: dict(),
            NfEaComCollectionTypes.EA_STEREOTYPES: dict(),
        }

    return \
        new_ea_objects_dictionary
