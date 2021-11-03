from bclearer_source.b_code.common_knowledge.content_operation_types import ContentOperationTypes
from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects
from bclearer_source.b_code.configurations.operation_configurations import OperationConfigurations


class ContentOperationConfigurations(
        OperationConfigurations):
    def __init__(
            self,
            content_operation_type: ContentOperationTypes,
            output_universe_short_name: str,
            default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects = None):
        super().__init__(
            operation_type=content_operation_type)

        self.output_universe_short_name = \
            output_universe_short_name

        self.default_digitalisation_level_stereotype = \
            default_digitalisation_level_stereotype

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
