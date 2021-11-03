from bclearer_source.b_code.substages.operations.b_evolve.convention_shift_operations.convention_shifters.common.list_of_contained_packages_of_a_package_getter import get_list_of_all_contained_packages_of_package
from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_common_source.code.services.reporting_service.reporters.log_with_datetime import log_message
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes
from pandas import DataFrame


# TODO: Use nf ea com table ..._ea_full_packages for this, rather than using recursion
def get_all_package_and_subpackages_classifiers(
        content_universe: NfEaComUniverses,
        package_ea_guid: str) \
        -> DataFrame:
    content_universe_ea_packages = \
        content_universe.nf_ea_com_registry.get_ea_packages()

    nf_uuids_column_name = \
        NfColumnTypes.NF_UUIDS.column_name

    list_of_package_ea_guids = \
        content_universe_ea_packages[NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name].tolist()

    if package_ea_guid not in list_of_package_ea_guids:
        log_message(
            message='CONVENTION SHIFT OPERATION: Extract UML names to attributes - Cannot find package EA GUID: ' +
                    package_ea_guid)

        return \
            DataFrame()

    package_nf_uuid = \
        content_universe_ea_packages[
            content_universe_ea_packages[
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name] == package_ea_guid][nf_uuids_column_name].to_string(index=False).strip()

    all_packages_and_subpackages_nf_uuids_set = \
        {package_nf_uuid}

    all_packages_and_subpackages_nf_uuids_set = \
        get_list_of_all_contained_packages_of_package(
            ea_packages_table=content_universe_ea_packages,
            package_nf_uuid=package_nf_uuid,
            set_of_all_packages_and_subpackages=all_packages_and_subpackages_nf_uuids_set)

    content_universe_ea_classifiers = \
        content_universe.nf_ea_com_registry.get_ea_classifiers()

    parent_ea_element_column_name = \
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name

    ea_object_type_column_name = \
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name

    domain_objects_classifiers_table = \
        content_universe_ea_classifiers[
            content_universe_ea_classifiers[parent_ea_element_column_name].isin(
                all_packages_and_subpackages_nf_uuids_set)]

    domain_classes_classifiers_table = \
        domain_objects_classifiers_table[
            domain_objects_classifiers_table[ea_object_type_column_name] == EaElementTypes.CLASS.type_name]

    # TODO: Track the export to EA to check where and why the EA GUIDs are being deleted/changed
    # TODO: Reformat instrument_and_visualize to export to EA without deleting/changing the EA GUIDs
    #  - look at AMis test "csv assemblies"

    return \
        domain_classes_classifiers_table
