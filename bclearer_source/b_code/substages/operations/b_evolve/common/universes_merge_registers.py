from bclearer_source.b_code.substages.operations.b_evolve.common.universe_aligner import align_universes
from nf_ea_common_tools_source.b_code.services.general.nf_ea.com.nf_ea_com_universes import NfEaComUniverses

ALIGNED_UNIVERSE_SHORT_NAME_SUFFIX = \
    '_aligned'


class UniversesMergeRegisters:
    def __init__(
            self,
            universe_1: NfEaComUniverses,
            universe_2: NfEaComUniverses,
            context: str):
        primary_universe, aligned_universe = \
            UniversesMergeRegisters.__classify_universes(
                universe_1=universe_1,
                universe_2=universe_2)

        self.primary_universe = \
            primary_universe

        self.aligned_universe = \
            aligned_universe

        self.aligned_to_primary_universe_nf_uuids_map = dict()

        align_universes(
            universe_merge_register=self,
            context=context)

    @staticmethod
    def __classify_universes(
            universe_1: NfEaComUniverses,
            universe_2: NfEaComUniverses):
        primary_universe = \
            universe_1

        aligned_universe_short_name = \
            universe_2.ea_repository.short_name + ALIGNED_UNIVERSE_SHORT_NAME_SUFFIX

        aligned_universe = \
            universe_2.copy(
                short_name=aligned_universe_short_name)

        return \
            primary_universe, aligned_universe
