from bclearer_source.b_code.common_knowledge.operation_types import OperationTypes
from enum import auto
from enum import unique


@unique
class ConventionShiftOperationTypes(
        OperationTypes):
    OBJECTS_TO_CLASSES = auto()
    UML_NAME_TO_NAMED_OBJECT = auto()
    ATTRIBUTE_NAME_TO_NAMED_OBJECT = auto()
    GENERALISE_NAMES = auto()
    SEPARATE_STANDARD_NAMES_AND_INSTANCES = auto()
    SEPARATE_BESPOKE_NAMES_AND_INSTANCES = auto()
    SEPARATE_STANDARD_INSTANCES_AND_EXEMPLARS = auto()
    SEPARATE_BESPOKE_INSTANCES_AND_EXEMPLARS = auto()
    UNIVERSE_TO_SEMANTICALLY_GROUNDED_DIGITALISATION_LEVEL = auto()

    def __operation_name(
            self) \
            -> str:
        operation_name = \
            operation_name_mapping[self]

        return \
            operation_name

    operation_name = \
        property(
            fget=__operation_name)


operation_name_mapping = \
    {
        ConventionShiftOperationTypes.OBJECTS_TO_CLASSES: 'shift_from_objects_to_classes',
        ConventionShiftOperationTypes.UML_NAME_TO_NAMED_OBJECT: 'shift_from_uml_name_to_named_object',
        ConventionShiftOperationTypes.ATTRIBUTE_NAME_TO_NAMED_OBJECT: 'shift_from_attribute_name_to_name_object',
        ConventionShiftOperationTypes.GENERALISE_NAMES: 'generalise_names',
        ConventionShiftOperationTypes.SEPARATE_STANDARD_NAMES_AND_INSTANCES: 'separate_standard_names_and_instances',
        ConventionShiftOperationTypes.SEPARATE_BESPOKE_NAMES_AND_INSTANCES: 'separate_bespoke_names_and_instances',
        ConventionShiftOperationTypes.SEPARATE_STANDARD_INSTANCES_AND_EXEMPLARS: 'separate_standard_instances_and_exemplars',
        ConventionShiftOperationTypes.SEPARATE_BESPOKE_INSTANCES_AND_EXEMPLARS: 'separate_bespoke_instances_and_exemplars',
        ConventionShiftOperationTypes.UNIVERSE_TO_SEMANTICALLY_GROUNDED_DIGITALISATION_LEVEL: 'shift_universe_to_semantically_grounded'
    }
