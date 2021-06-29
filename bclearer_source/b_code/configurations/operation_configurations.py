from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes


class OperationConfigurations:
    def __init__(
            self,
            operation_type: OperationTypes):
        self.operation_type = \
            operation_type

    def __enter__(
            self):
        return \
            self

    def __exit__(
            self,
            exception_type,
            exception_value,
            traceback):
        pass
