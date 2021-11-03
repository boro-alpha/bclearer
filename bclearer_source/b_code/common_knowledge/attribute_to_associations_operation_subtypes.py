from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes
from enum import auto
from enum import unique


@unique
class AttributeToAssociationOperationSubtypes(
        OperationTypes):
    DIRECT_FOREIGN_TABLE = auto()
    SUBTYPE_OF_FOREIGN_TABLE = auto()

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
        AttributeToAssociationOperationSubtypes.DIRECT_FOREIGN_TABLE: 'direct_foreign_table',
        AttributeToAssociationOperationSubtypes.SUBTYPE_OF_FOREIGN_TABLE: 'subtype_of_foreign_table'
    }
