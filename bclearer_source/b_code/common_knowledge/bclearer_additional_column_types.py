from enum import auto
from enum import unique
from nf_common_source.code.nf.types.column_types import ColumnTypes


@unique
class BclearerAdditionalColumnTypes(
        ColumnTypes):
    NAMING_SPACE_NF_UUIDS = \
        auto()

    NAME_INSTANCE_TYPE_NF_UUIDS = \
        auto()

    OWNING_OBJECT_NAMES = \
        auto()

    def __column_name(
            self) \
            -> str:
        column_name = \
            column_name_mapping[self]

        return \
            column_name

    column_name = \
        property(
            fget=__column_name)


column_name_mapping = \
    {
        BclearerAdditionalColumnTypes.NAMING_SPACE_NF_UUIDS: 'naming_space_nf_uuids',
        BclearerAdditionalColumnTypes.NAME_INSTANCE_TYPE_NF_UUIDS: 'name_instance_type_nf_uuids',
        BclearerAdditionalColumnTypes.OWNING_OBJECT_NAMES: 'owning_object_names'
    }
