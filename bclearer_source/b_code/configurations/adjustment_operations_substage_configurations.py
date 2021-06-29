class AdjustmentOperationsSubstageConfigurations:
    def __init__(
            self,
            operation_configurations: set):
        self.operation_configurations = \
            operation_configurations

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
