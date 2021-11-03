from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from enum import unique
from enum import auto


@unique
class BclearerMatchedEaObjects(
        MatchedEaObjects):
    BCLEARER_FOUNDATION_COMMON_RESERVED_NAMES = \
        auto()

    NAMES = \
        auto()

    NAME_INSTANCES = \
        auto()

    NAME_EXEMPLARS = \
        auto()

    CHARACTER_STRINGS = \
        auto()

    MODEL_PACKAGE = \
        auto()

    NAMED_BY_STEREOTYPE = \
        auto()

    NAME_TYPES_INSTANCES_STEREOTYPE = \
        auto()

    EXEMPLIFIED_BY_STEREOTYPE = \
        auto()

    NAME_EXEMPLAR_STEREOTYPE = \
        auto()

    def __object_name(
            self) \
            -> str:
        object_name = \
            object_name_mapping[self]

        return \
            object_name

    def __ea_guid(
            self) \
            -> str:
        ea_guid = \
            ea_guid_mapping[self]

        return \
            ea_guid

    object_name = \
        property(
            fget=__object_name)

    ea_guid = \
        property(
            fget=__ea_guid)


object_name_mapping = \
    {
        BclearerMatchedEaObjects.BCLEARER_FOUNDATION_COMMON_RESERVED_NAMES: 'bCLEARer Foundation Common Reserved Names',
        BclearerMatchedEaObjects.NAMES: 'Names',
        BclearerMatchedEaObjects.NAME_INSTANCES: 'Name Instances',
        BclearerMatchedEaObjects.NAME_EXEMPLARS: 'Name Exemplars',
        BclearerMatchedEaObjects.CHARACTER_STRINGS: 'Character Strings',
        BclearerMatchedEaObjects.MODEL_PACKAGE: 'bCLEARer Foundation Package',
        BclearerMatchedEaObjects.NAMED_BY_STEREOTYPE: 'named by',
        BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE: 'name types-instances',
        BclearerMatchedEaObjects.EXEMPLIFIED_BY_STEREOTYPE: 'exemplified by',
        BclearerMatchedEaObjects.NAME_EXEMPLAR_STEREOTYPE: 'name exemplar'
    }


ea_guid_mapping = \
    {
        BclearerMatchedEaObjects.BCLEARER_FOUNDATION_COMMON_RESERVED_NAMES: '{7fd8c00c-2b46-11eb-86df-983b8f873eed}',
        BclearerMatchedEaObjects.NAMES: '{7fd9834a-2b46-11eb-84e7-983b8f873eed}',
        BclearerMatchedEaObjects.NAME_INSTANCES: '{25E1D82C-87F0-4585-9401-B839DF7F17AB}',
        BclearerMatchedEaObjects.NAME_EXEMPLARS: '{07846B84-EF0C-4596-A54D-6E389DDB247D}',
        BclearerMatchedEaObjects.CHARACTER_STRINGS: '{6054422D-3626-4351-97E3-11EB0852BD2D}',
        BclearerMatchedEaObjects.MODEL_PACKAGE: '{72bb7541-2b46-11eb-96c9-983b8f873eed}',
        BclearerMatchedEaObjects.NAMED_BY_STEREOTYPE: '{7CBE78A4-6CDA-49c4-82CC-AB89A6AF99D9}',
        BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE: '{44D7CCD7-3943-4b8f-92A6-67D0BB0BD12F}',
        BclearerMatchedEaObjects.EXEMPLIFIED_BY_STEREOTYPE: '{A8B38219-0B26-46f9-82EC-E7556CCE2120}',
        BclearerMatchedEaObjects.NAME_EXEMPLAR_STEREOTYPE: '{1C49F9D8-5D83-4dcc-B49A-665E759A6EB1}'
    }
