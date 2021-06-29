from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from bclearer_source.b_code.substages.operations.common.nf_uuid_from_ea_guid_from_collection_getter import get_nf_uuid_from_ea_guid_from_collection
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def get_instances_nf_uuids_of_matched_type(
        nf_ea_com_universe: NfEaComUniverses,
        matched_type: MatchedEaObjects) \
        -> set:
    matched_type_nf_uuid = \
        get_nf_uuid_from_ea_guid_from_collection(
            nf_ea_com_universe=nf_ea_com_universe,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            ea_guid=matched_type.ea_guid)

    instances_nf_uuids = \
        get_instances_nf_uuids_of_type_nf_uuid(
            nf_ea_com_universe=nf_ea_com_universe,
            nf_uuid=matched_type_nf_uuid)

    return \
        instances_nf_uuids


def get_instances_nf_uuids_of_type_nf_uuid(
        nf_ea_com_universe: NfEaComUniverses,
        nf_uuid: str) \
        -> set:
    ea_connectors = \
        nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()

    ea_dependencies = \
        ea_connectors[ea_connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    filtered_dependencies = \
        ea_dependencies[ea_dependencies[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name] == nf_uuid]

    instances_nf_uuids = \
        set(filtered_dependencies[NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name])

    return \
        instances_nf_uuids
