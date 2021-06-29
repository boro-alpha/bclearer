from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects


class BespokeNameToInstanceConfigurationObjects:
    def __init__(
            self,
            matched_naming_space_type: MatchedEaObjects,
            name_instance_attribute_name: str = None,
            matched_name_instance_type: MatchedEaObjects = None,
            package_name: str = None):

        self.matched_naming_space_type = \
            matched_naming_space_type

        self.name_instance_attribute_name = \
            name_instance_attribute_name

        self.matched_name_instance_type = \
            matched_name_instance_type

        self.package_name = \
            package_name

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
