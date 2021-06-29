from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes
from enum import auto
from enum import unique


@unique
class AdjustmentOperationTypes(
        OperationTypes):
    REMOVE_ATTRIBUTES = auto()
    CONVERT_ATTRIBUTES_TO_ASSOCIATIONS = auto()

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
        AdjustmentOperationTypes.REMOVE_ATTRIBUTES: 'remove_attributes',
        AdjustmentOperationTypes.CONVERT_ATTRIBUTES_TO_ASSOCIATIONS: 'convert_attributes_to_associations'
    }
