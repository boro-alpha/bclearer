from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from bclearer_source.b_code.configurations.universe_modification_configuration_objects import \
    UniverseModificationConfigurationObjects


class AddDependencyToInstancesOfTypeConfigurationObjects(
        UniverseModificationConfigurationObjects):
    def __init__(
            self,
            matched_target_type: MatchedEaObjects,
            matched_source_objects_type: MatchedEaObjects):
        super().__init__()

        self.matched_target_type = \
            matched_target_type

        self.matched_source_objects_type = \
            matched_source_objects_type

    def get_matched_target_type(
            self) \
            -> MatchedEaObjects:
        return \
            self.matched_target_type

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
