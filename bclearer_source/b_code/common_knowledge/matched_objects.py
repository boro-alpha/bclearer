from enum import Enum
from enum import unique


@unique
class MatchedEaObjects(
        Enum):
    def __object_name(
            self) \
            -> str:
        raise \
            NotImplementedError

    def __ea_guid(
            self) \
            -> str:
        raise \
            NotImplementedError

    object_name = \
        property(
            fget=__object_name)

    ea_guid = \
        property(
            fget=__ea_guid)
