class AttributeToScopePatternConfigurationObjects:
    def __init__(
            self,
            attributed_type_name: str,
            attributed_type_ea_guid: str,
            attribute_name: str,
            attribute_ea_guid: str,
            scoping_type: str,
            scoping_type_name: str):

        self.attributed_type_name = \
            attributed_type_name

        self.attributed_type_ea_guid = \
            attributed_type_ea_guid

        self.attribute_name = \
            attribute_name

        self.attribute_ea_guid = \
            attribute_ea_guid

        self.scoping_type = \
            scoping_type

        self.scoping_type_name = \
            scoping_type_name

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
