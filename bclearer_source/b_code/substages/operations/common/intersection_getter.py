from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def get_intersection_of_dependency_and_association_linked(
        nf_ea_com_universe: NfEaComUniverses,
        linked_by_dependency_nf_uuid: str,
        linked_by_association_nf_uuid: str) \
        -> str:
    connected_by_dependency_set = \
        get_connected_classifiers(
            nf_ea_com_universe=nf_ea_com_universe,
            classifier_nf_uuid=linked_by_dependency_nf_uuid,
            connection_type=EaConnectorTypes.DEPENDENCY,
            connected_end_type=NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS)

    connected_by_association_set = \
        get_connected_classifiers(
            nf_ea_com_universe=nf_ea_com_universe,
            classifier_nf_uuid=linked_by_association_nf_uuid,
            connection_type=EaConnectorTypes.ASSOCIATION,
            connected_end_type=NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS)

    intersection = \
        list(
            connected_by_dependency_set & connected_by_association_set)

    if len(intersection) == 1:
        return \
            intersection[0]

    else:
        raise ValueError(
            'Too many objects in intersection')


def get_connected_classifiers(
        nf_ea_com_universe: NfEaComUniverses,
        classifier_nf_uuid: str,
        connection_type: EaConnectorTypes,
        connected_end_type: NfEaComColumnTypes) \
        -> set:
    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_CONNECTORS]

    connections = \
        ea_connectors[
            ea_connectors[connected_end_type.column_name] == classifier_nf_uuid]

    connections_by_type = \
        connections[connections[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == connection_type.type_name]

    if connected_end_type == NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS:
        connected_classifiers = \
            set(connections_by_type[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name])

    elif connected_end_type == NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS:
        connected_classifiers = \
            set(connections_by_type[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name])

    else:
        raise TypeError(
            'Invalid connector end column: ' + connected_end_type.column_name)

    return \
        connected_classifiers
