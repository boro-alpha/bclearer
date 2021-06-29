from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects


class GeneraliseNamesConfigurationObjects:
    def __init__(
            self,
            matched_named_object: MatchedEaObjects,
            matched_naming_space: MatchedEaObjects,
            matched_name: MatchedEaObjects,
            matched_named_by_stereotype: MatchedEaObjects):

        self.matched_named_object = \
            matched_named_object

        self.matched_naming_space = \
            matched_naming_space

        self.matched_name = \
            matched_name

        self.matched_named_by_stereotype = \
            matched_named_by_stereotype

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
