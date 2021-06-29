from bclearer_source.b_code.common_knowledge.content_operation_types import ContentOperationTypes
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations


class ContentOperationConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            content_operation_type: ContentOperationTypes,
            output_universe_short_name: str):
        super().__init__(
            operation_type=content_operation_type)

        self.output_universe_short_name = \
            output_universe_short_name

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
