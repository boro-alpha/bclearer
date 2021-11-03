from bclearer_source.b_code.substages.operations.common.ea_guid_from_nf_uuid_creator import create_ea_guid_from_nf_uuid
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.identification_services.uuid_service.uuid_helpers.uuid_factory import create_new_uuid
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import EaTPackageColumnTypes
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from pandas import DataFrame, set_option


def create_new_subpackage_if_not_exist(
        nf_ea_com_universe_ea_packages: DataFrame,
        new_ea_packages_dictionary: dict,
        package_nf_uuid: str,
        new_subpackage_name: str) \
        -> str:
    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    object_name_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name

    contained_ea_packages_column_name = \
        NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name

    list_of_first_level_contained_packages = \
        nf_ea_com_universe_ea_packages[
            nf_ea_com_universe_ea_packages[
                nf_uuids_column_name] == package_nf_uuid][contained_ea_packages_column_name].tolist()[0]

    ea_packages_sliced_to_first_level_contained_packages = \
        nf_ea_com_universe_ea_packages[
            nf_ea_com_universe_ea_packages[
                nf_uuids_column_name].isin(list_of_first_level_contained_packages)]

    list_of_first_level_contained_packages_names = \
        ea_packages_sliced_to_first_level_contained_packages[object_name_column_name].tolist()

    name_package_already_created_in_parent_package_nf_uuid = \
        None

    for new_ea_packages_row_dictionary in new_ea_packages_dictionary.values():
        if new_ea_packages_row_dictionary[NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name] == package_nf_uuid and \
                new_ea_packages_row_dictionary[object_name_column_name] == new_subpackage_name:
            name_package_already_created_in_parent_package_nf_uuid = new_ea_packages_row_dictionary[nf_uuids_column_name]

    if new_subpackage_name in list_of_first_level_contained_packages_names:
        new_subpackage_nf_uuid_row = \
            ea_packages_sliced_to_first_level_contained_packages[
                ea_packages_sliced_to_first_level_contained_packages[object_name_column_name] == new_subpackage_name]

        new_subpackage_nf_uuid = \
            new_subpackage_nf_uuid_row[nf_uuids_column_name].to_string(index=False).strip()

        return \
            new_subpackage_nf_uuid

    elif name_package_already_created_in_parent_package_nf_uuid is not None:
        return name_package_already_created_in_parent_package_nf_uuid

    else:
        new_subpackage_nf_uuid = \
            __add_new_package_row(
                ea_packages_table=nf_ea_com_universe_ea_packages,
                new_ea_packages_dictionary=new_ea_packages_dictionary,
                parent_package_nf_uuid=package_nf_uuid,
                new_package_name=new_subpackage_name)

        list_of_first_level_contained_packages_updated = \
            list_of_first_level_contained_packages.append(
                new_subpackage_nf_uuid)

        nf_ea_com_universe_ea_packages[
            nf_ea_com_universe_ea_packages[
                nf_uuids_column_name] == package_nf_uuid][contained_ea_packages_column_name] = \
            list_of_first_level_contained_packages_updated

        return \
            new_subpackage_nf_uuid


def __add_new_package_row(
        ea_packages_table: DataFrame,
        new_ea_packages_dictionary: dict,
        parent_package_nf_uuid: str,
        new_package_name: str) \
        -> str:
    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    ea_guid_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name

    object_name_column_name = \
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name

    new_package_nf_uuid = \
        create_new_uuid()

    new_package_ea_guid = \
        create_ea_guid_from_nf_uuid(
            nf_uuid=new_package_nf_uuid)

    parent_package_ea_guid = \
        ea_packages_table[
            ea_packages_table[
                nf_uuids_column_name] == parent_package_nf_uuid][
            ea_guid_column_name].to_string(index=False).strip()

    parent_package_name = \
        ea_packages_table[
            ea_packages_table[
                nf_uuids_column_name] == parent_package_nf_uuid][
            object_name_column_name].to_string(index=False).strip()

    # Note: Pandas truncates long strings. The following instructions prevents pandas from doing that.
    # TODO: Consider to move this option higher in the hierarchy
    set_option(
        'display.max_colwidth', None)

    parent_package_ea_package_path = \
        ea_packages_table[
            ea_packages_table[
                nf_uuids_column_name] == parent_package_nf_uuid][
            'ea_package_path'].to_string(index=False).strip()

    new_package_ea_package_path = \
        parent_package_ea_package_path + '/' + new_package_name

    ea_packages_row_dictionary = \
        {
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name: new_package_ea_guid,
            'ea_package_path': new_package_ea_package_path,
            'parent_package_ea_guid': parent_package_ea_guid,
            'parent_package_name': parent_package_name,
            nf_uuids_column_name: new_package_nf_uuid,
            NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name: [],
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name: EaElementTypes.PACKAGE.type_name,
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: [],
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: [],
            NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS.column_name: [],
            NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS.column_name: [],
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name: parent_package_nf_uuid,
            NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
            object_name_column_name: new_package_name,
            ea_guid_column_name: new_package_ea_guid
        }

    new_ea_packages_dictionary[len(new_ea_packages_dictionary) + 1] = \
        ea_packages_row_dictionary

    return \
        new_package_nf_uuid
