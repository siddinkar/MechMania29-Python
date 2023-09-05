from dataclasses import asdict, dataclass
import json
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type
from game.util.position import Position


@dataclass
class MoveAction:
    """
    Defines where a character will move
    """

    executing_character_id: str
    destination: Position

    def from_json(blob: object) -> "MoveAction":
        try:
            assert_blob_has_key_of_type(blob, "executingCharacterId", str)
            assert_blob_has_key_of_type(blob, "destination", dict)
            action = MoveAction(
                blob["executingCharacterId"],
                Position.from_json(blob["destination"]),
            )
        except:
            print("Failed to validate MoveAction json")
            raise

        return action
