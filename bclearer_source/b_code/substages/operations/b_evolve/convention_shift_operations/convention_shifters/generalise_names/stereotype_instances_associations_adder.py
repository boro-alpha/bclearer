from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.dataframe_service.dataframe_mergers import inner_merge_dataframes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_connector_types import EaConnectorTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_property_types import EaPropertyTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import NfEaComCollectionTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses


def add_stereotype_to_instances_associations(
        nf_ea_com_universe: NfEaComUniverses,
        type_nf_uuid: str,
        stereotype_nf_uuid: str) \
        -> None:
    connectors = \
        nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[NfEaComCollectionTypes.EA_CONNECTORS]

    connectors_to_type = \
        connectors[connectors[NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name] == type_nf_uuid]

    dependencies_to_type = \
        connectors_to_type[connectors_to_type[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.DEPENDENCY.type_name]

    associations = \
        connectors[connectors[NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name] == EaConnectorTypes.ASSOCIATION.type_name]

    linked_relations = \
        inner_merge_dataframes(
            master_dataframe=dependencies_to_type,
            master_dataframe_key_columns=[
                NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name],
            merge_suffixes=['_dependency', '_association'],
            foreign_key_dataframe=associations,
            foreign_key_dataframe_fk_columns=[
                NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name],
            foreign_key_dataframe_other_column_rename_dictionary=
            {
                NfColumnTypes.NF_UUIDS.column_name: NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
            })

    new_stereotype_usages = \
        linked_relations.filter(
            items=[NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name])

    new_stereotype_usages[NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name] = \
        EaPropertyTypes.CONNECTOR_PROPERTY.type_name

    new_stereotype_usages['stereotype_nf_uuids'] = \
        stereotype_nf_uuid

    nf_ea_com_universe.nf_ea_com_registry.update(
        collection_type=NfEaComCollectionTypes.STEREOTYPE_USAGE,
        new_collection=new_stereotype_usages)
