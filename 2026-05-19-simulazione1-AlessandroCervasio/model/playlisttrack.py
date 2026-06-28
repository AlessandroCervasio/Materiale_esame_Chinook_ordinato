from dataclasses import dataclass


@dataclass
class Playlisttrack:
    PlaylistId: int
    TrackId: int
    def __hash__(self):
        return hash((self.PlaylistId, self.TrackId))
    def __eq__(self, other):
        return (self.PlaylistId, self.TrackId)==(other.PlaylistId, other.TrackId)
    def __str__(self):
        return f"{self.PlaylistId} -- {self.TrackId}"