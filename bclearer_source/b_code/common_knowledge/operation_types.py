from enum import Enum


class OperationTypes(
        Enum):
    def __operation_name(
            self) \
            -> str:
        raise \
            NotImplementedError

    operation_name = \
        property(
            fget=__operation_name)


