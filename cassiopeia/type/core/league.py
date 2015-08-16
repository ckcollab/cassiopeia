import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.league

@cassiopeia.type.core.common.inheritdocs
class Series(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.MiniSeries

    def __str__(self):
        return progress

    @property
    def losses(self):
        """Number of current losses in the mini series"""
        return self.data.losses

    @property
    def progress(self):
        """String showing the current, sequential mini series progress where 'W' represents a win, 'L' epresents a loss, and 'N' represents a game that hasn't been played yet"""
        return self.data.progress

    @property
    def wins_required(self):
        """Number of wins required for promotion"""
        return self.data.target

    @property
    def wins(self):
        """Number of current wins in the series"""
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class Entry(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.LeagueEntry

    def __str__(self):
        return "{summoner} ({lp} LP)".format(summoner=self.summoner_name, lp=self.league_points)

    @property
    def division(self):
        """The League division of the participant"""
        return cassiopeia.type.core.common.Division(self.data.division) if self.data.division else None

    @property
    def fresh_blood(self):
        """Specifies if the participant is fresh blood (ie if they have just joined the league)"""
        return self.data.isFreshBlood

    @property
    def hot_streak(self):
        """Specifies if the participant is on a hot streak"""
        return self.data.isHotStreak

    @property
    def inactive(self):
        """Specifies if the participant is inactive"""
        return self.data.isInactive

    @property
    def veteran(self):
        """Specifies if the participant is a veteran (ie they have been in this league for a long time)"""
        return self.data.isVeteran

    @property
    def league_points(self):
        """The league points of the participant"""
        return self.data.leaguePoints

    @property
    def losses(self):
        """The number of losses for the participant"""
        return self.data.losses

    @cassiopeia.type.core.common.lazyproperty
    def series(self):
        """Series data for the participant. Only present if the participant is currently in a mini series"""
        return Series(self.data.miniSeries) if self.data.miniSeries else None

    @property
    def summoner(self):
        """The Summoner represented by this entry. None if this entry is for a team"""
        if(not self.data.playerOrTeamId):
            return None

        try:
            id_ = int(self.data.playerOrTeamId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except(ValueError):
            return None

    @property
    def team(self):
        """The Team represented by this entry. None if this entry is for a summoner"""
        if(not self.data.playerOrTeamId):
            return None

        try:
            int(self.data.playerOrTeamId)
            return None
        except(ValueError):
            return cassiopeia.riotapi.get_team_by_id(self.data.playerOrTeamId)

    @property
    def summoner_name(self):
        """The name of the summoner represented by this entry. An empty string if this entry is for a team"""
        if(not self.data.playerOrTeamId):
            return ""

        try:
            int(self.data.playerOrTeamId)
            return self.data.playerOrTeamName
        except(ValueError):
            return ""

    @property
    def team_name(self):
        """The name of the team represented by this entry. An empty string if this entry is for a summoner"""
        try:
            int(self.data.playerOrTeamId)
            return ""
        except(ValueError):
            return self.data.playerOrTeamName

    @property
    def wins(self):
        """The number of wins for the participant"""
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class League(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.League
    
    def __str__(self):
        return "{name} ({tier})".format(name=self.name, tier=self.tier)

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    @cassiopeia.type.core.common.lazyproperty
    def entries(self):
        """A list of the requested league entries, sorted by LP"""
        return sorted([Entry(entry) for entry in self.data.entries], key=lambda entry: entry.league_points, reverse=True)

    @property
    def name(self):
        """The name of the league"""
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def participant_entry(self):
        """The Entry for the relevant team or summoner that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested"""
        for entry in self.entries:
            if(entry.data.playerOrTeamId == self.data.participantId):
                return entry
        return None

    @property
    def summoner(self):
        """The relevant Summoner that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested or the participant is a team."""
        if(not self.data.participantId):
            return None

        try:
            id_ = int(self.data.participantId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except(ValueError):
            return None

    @property
    def team(self):
        """The relevant Team that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested or the participant is a summoner."""
        if(not self.data.participantId):
            return None

        try:
            int(self.data.participantId)
            return None
        except(ValueError):
            return cassiopeia.riotapi.get_team_by_id(self.data.participantId)

    @property
    def queue(self):
        """The league's Queue type"""
        return cassiopeia.type.core.common.Queue(self.data.queue) if self.data.queue else None

    @property
    def tier(self):
        """The league's Tier"""
        return cassiopeia.type.core.common.Tier(self.data.tier) if self.data.tier else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Series.dto_type = cassiopeia.type.dto.league.MiniSeries
    Entry.dto_type = cassiopeia.type.dto.league.LeagueEntry
    League.dto_type = cassiopeia.type.dto.league.League
