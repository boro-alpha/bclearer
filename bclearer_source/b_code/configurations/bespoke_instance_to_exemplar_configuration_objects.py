from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects


class BespokeInstanceToExemplarConfigurationObjects:
    def __init__(
            self,
            matched_name_instance_instance: MatchedEaObjects,
            name_exemplar_attribute_name: str):

        self.matched_name_instance_instance = \
            matched_name_instance_instance

        self.name_exemplar_attribute_name = \
            name_exemplar_attribute_name

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
