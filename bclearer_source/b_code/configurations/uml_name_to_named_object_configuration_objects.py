from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects


class UmlNameToNamedObjectConfigurationObjects:
    def __init__(
            self,
            matched_package: MatchedEaObjects,
            matched_naming_space: MatchedEaObjects):
        self.matched_package = \
            matched_package

        self.matched_naming_space = \
            matched_naming_space

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
