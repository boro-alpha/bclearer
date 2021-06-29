from bclearer_source.b_code.common_knowledge.content_operation_types import ContentOperationTypes
from bclearer_source.b_code.configurations.content_operation_configurations import ContentOperationConfigurations
from bclearer_source.b_code.substages.operations.b_evolve.content_operations.merge_universes.universe_merger import merge_universes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses
from nf_ea_common_tools_source.b_code.services.session.orchestrators.ea_tools_session_managers import EaToolsSessionManagers
from nf_ea_common_tools_source.b_code.services.session.processes.creators.empty_nf_ea_com_universe_creator import create_empty_nf_ea_universe


class ContentOperationsSubstages:
    def __init__(
            self,
            ea_tools_session_manager: EaToolsSessionManagers,
            content_operation_configuration: ContentOperationConfigurations,
            content_1_universe: NfEaComUniverses,
            content_2_universe: NfEaComUniverses):
        self.ea_tools_session_manager = \
            ea_tools_session_manager

        self.content_operation_configuration = \
            content_operation_configuration

        self.content_1_universe = \
            content_1_universe

        self.content_2_universe = \
            content_2_universe

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

    def run(
            self) \
            -> NfEaComUniverses:
        output_universe = \
            create_empty_nf_ea_universe(
                ea_tools_session_manager=self.ea_tools_session_manager,
                short_name=self.content_operation_configuration.output_universe_short_name)

        if self.content_operation_configuration.operation_type == ContentOperationTypes.MERGE_UNIVERSES:
            merge_universes(
                content_1_universe=self.content_1_universe,
                content_2_universe=self.content_2_universe,
                output_universe=output_universe,
                context=self.__class__.__name__)

        return \
            output_universe
