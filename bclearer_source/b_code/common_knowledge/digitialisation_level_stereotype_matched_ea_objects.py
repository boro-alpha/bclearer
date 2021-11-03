from bclearer_source.b_code.common_knowledge.matched_objects import MatchedEaObjects
from enum import unique
from enum import auto


@unique
class DigitalisationLevelStereotypeMatchedEaObjects(
        MatchedEaObjects):
    DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_2_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_3_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_4_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_5_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_6_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_7_CLASS_STEREOTYPE = \
        auto()

    DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE = \
        auto()

    @classmethod
    def get_ea_guids(cls) -> set:
        ea_guids = \
            set(
                ea_guid_mapping.values())

        return \
            ea_guids

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

    def __style(
            self) \
            -> str:
        style = \
            digitalisation_level_styles[self]

        return \
            style

    object_name = \
        property(
            fget=__object_name)

    ea_guid = \
        property(
            fget=__ea_guid)

    style = \
        property(
            fget=__style)


object_name_mapping = \
    {
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE: 'DL1',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_2_CLASS_STEREOTYPE: 'DL2',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_3_CLASS_STEREOTYPE: 'DL3',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_4_CLASS_STEREOTYPE: 'DL4',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_5_CLASS_STEREOTYPE: 'DL5',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_6_CLASS_STEREOTYPE: 'DL6',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_7_CLASS_STEREOTYPE: 'DL7',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE: 'DL8'
    }


ea_guid_mapping = \
    {
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE: '{FF73ABA9-DE5C-4eeb-918C-DECA01FF7280}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_2_CLASS_STEREOTYPE: '{0AA699E0-7794-4aea-8F27-EED1706BB74D}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_3_CLASS_STEREOTYPE: '{2A9FD9A6-9D8F-421c-BF26-A3FBA21268B4}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_4_CLASS_STEREOTYPE: '{24129ADB-A8B8-42e8-8EBB-2954690FB64D}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_5_CLASS_STEREOTYPE: '{EE83A38C-E442-498b-A594-26699B46DC0F}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_6_CLASS_STEREOTYPE: '{5D0561A8-ECB7-4016-AD3F-8F80135F5CB9}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_7_CLASS_STEREOTYPE: '{5BD3B142-98DF-4c94-B740-D000DCB4A009}',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE: '{8A1027F5-6CA2-49d8-A933-1DF26D07642C}'
    }


digitalisation_level_styles = \
    {
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE: '<STYLE fill="1837750" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_2_CLASS_STEREOTYPE: '<STYLE fill="3225056" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_3_CLASS_STEREOTYPE: '<STYLE fill="5007615" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_4_CLASS_STEREOTYPE: '<STYLE fill="170211" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_5_CLASS_STEREOTYPE: '<STYLE fill="2604528" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_6_CLASS_STEREOTYPE: '<STYLE fill="6740735" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_7_CLASS_STEREOTYPE: '<STYLE fill="8310410" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>',
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE: '<STYLE fill="4428080" text="-1" border="-1" groupname="Digitalisation Level Group" type="metafile"/>'
    }


digitalisation_level_order = \
    {
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_1_CLASS_STEREOTYPE: 1,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_2_CLASS_STEREOTYPE: 2,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_3_CLASS_STEREOTYPE: 3,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_4_CLASS_STEREOTYPE: 4,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_5_CLASS_STEREOTYPE: 5,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_6_CLASS_STEREOTYPE: 6,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_7_CLASS_STEREOTYPE: 7,
        DigitalisationLevelStereotypeMatchedEaObjects.DIGITALISATION_LEVEL_8_CLASS_STEREOTYPE: 8
    }
