from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes
from enum import auto
from enum import unique


@unique
class ContentOperationTypes(
        OperationTypes):
    MERGE_UNIVERSES = auto()

    def __operation_name(
            self) \
            -> str:
        operation_name = \
            operation_name_mapping[self]

        return \
            operation_name

    operation_name = \
        property(
            fget=__operation_name)


operation_name_mapping = \
    {
        ContentOperationTypes.MERGE_UNIVERSES: 'merge_universes'
    }
