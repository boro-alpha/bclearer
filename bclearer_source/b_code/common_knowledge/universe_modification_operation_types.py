from enum import unique, auto

from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes


@unique
class UniverseModificationOperationTypes(
        OperationTypes):
    ADD_DEPENDENCY_TO_INSTANCES_OF_TYPE = auto()

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
        UniverseModificationOperationTypes.ADD_DEPENDENCY_TO_INSTANCES_OF_TYPE: 'add_dependency_to_instances_of_type'
    }
