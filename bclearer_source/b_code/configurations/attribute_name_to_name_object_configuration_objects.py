from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects


class AttributeNameToNameObjectConfigurationObjects:
    def __init__(
            self,
            matched_naming_space_instance: MatchedEaObjects):

        self.matched_naming_space_instance = \
            matched_naming_space_instance

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
