from bclearer_source.b_code.substages.operations.common.classifier_adder import add_new_classifier_to_dictionary
from nf_ea_common_tools_source.b_code.nf_ea_common.common_knowledge.ea_element_types import EaElementTypes


def add_new_class_to_dictionary(
        new_classifier_dictionary: dict,
        package_nf_uuid: str,
        class_name: str) \
        -> str:
    class_nf_uuid = \
        add_new_classifier_to_dictionary(
            new_classifier_dictionary=new_classifier_dictionary,
            package_nf_uuid=package_nf_uuid,
            ea_element_type=EaElementTypes.CLASS,
            class_name=class_name)

    return \
        class_nf_uuid
