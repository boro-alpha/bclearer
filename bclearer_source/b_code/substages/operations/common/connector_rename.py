from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def rename_connector(
        nf_ea_com_universe: NfEaComUniverses,
        place_1_nf_uuid: str,
        place_2_nf_uuid: str,
        connector_type: EaConnectorTypes,
        connector_name: str) \
        -> None:
    connectors = \
        nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_CONNECTORS]

    connectors_connecting_place_1 = \
        connectors[connectors[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name] == place_1_nf_uuid]

    connectors_connecting_place_1_and_2 = \
        connectors_connecting_place_1[connectors_connecting_place_1[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name] == place_2_nf_uuid]

    connectors_connecting_place_1_and_2_of_type = \
        connectors_connecting_place_1_and_2[connectors_connecting_place_1_and_2[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == connector_type.type_name]

    connector_nf_uuid = \
        list(connectors_connecting_place_1_and_2_of_type[NfColumnTypes.NF_UUIDS.column_name])[0]

    connectors.loc[connectors[NfColumnTypes.NF_UUIDS.column_name] == connector_nf_uuid, NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name] = \
        connector_name

    nf_ea_com_universe.nf_ea_com_registry.replace_collection(
        collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
        collection=connectors)
