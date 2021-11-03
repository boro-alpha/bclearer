from bclearer_source.b_code.common_knowledge.digitialisation_level_stereotype_matched_ea_objects import \
    DigitalisationLevelStereotypeMatchedEaObjects


class LoadHdf5ModelConfigurations:
    def __init__(
            self,
            resource_namespace: str,
            resource_file_name: str,
            universe_short_name: str,
            default_digitalisation_level_stereotype: DigitalisationLevelStereotypeMatchedEaObjects = None,
            ea_guid_to_digitalisation_level_stereotype_dictionary: dict = None):
        self.resource_namespace = \
            resource_namespace

        self.resource_file_name = \
            resource_file_name

        self.universe_short_name = \
            universe_short_name

        self.default_digitalisation_level_stereotype = \
            default_digitalisation_level_stereotype

        self.ea_guid_to_digitalisation_level_stereotype_dictionary = \
            ea_guid_to_digitalisation_level_stereotype_dictionary

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
