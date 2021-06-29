class LoadHdf5ModelConfigurations:
    def __init__(
            self,
            resource_namespace: str,
            resource_file_name: str,
            universe_short_name: str,):
        self.resource_namespace = \
            resource_namespace

        self.resource_file_name = \
            resource_file_name

        self.universe_short_name = \
            universe_short_name

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
