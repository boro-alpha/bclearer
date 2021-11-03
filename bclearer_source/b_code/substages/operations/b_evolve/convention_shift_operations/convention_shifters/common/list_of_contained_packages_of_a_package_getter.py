from nf_common_source.code.nf.types.nf_column_types import NfColumnTypes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import NfEaComColumnTypes
from pandas import DataFrame


# TODO: This method may no longer be needed once the caller uses table ea_full_packages
def get_list_of_all_contained_packages_of_package(
        ea_packages_table: DataFrame,
        package_nf_uuid: str,
        set_of_all_packages_and_subpackages: set):
    list_of_contained_packages = \
        ea_packages_table[
            ea_packages_table[
                NfColumnTypes.NF_UUIDS.column_name] == package_nf_uuid][NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name].tolist()[0]

    set_of_contained_packages = \
        set(list_of_contained_packages)

    if len(set_of_contained_packages) == 0:
        return \
            set_of_all_packages_and_subpackages

    else:
        set_of_all_packages_and_subpackages = \
            set_of_all_packages_and_subpackages.union(
                set_of_contained_packages)

        for subpackage in set_of_contained_packages:
            set_of_subpackages = \
                get_list_of_all_contained_packages_of_package(
                    ea_packages_table=ea_packages_table,
                    package_nf_uuid=subpackage,
                    set_of_all_packages_and_subpackages=set_of_all_packages_and_subpackages)

            set_of_all_packages_and_subpackages = \
                set_of_all_packages_and_subpackages.union(set_of_subpackages)

        return \
            set_of_all_packages_and_subpackages
