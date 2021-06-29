class LoadEaModelConfigurations:
    def __init__(
            self,
            resource_namespace: str,
            resource_name: str,
            short_name: str,):
        self.resource_namespace = \
            resource_namespace

        self.resource_name = \
            resource_name

        self.short_name = \
            short_name

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
