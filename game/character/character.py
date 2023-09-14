from dataclasses import dataclass
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type
from game.util.position import Position


@dataclass
class Character:
    """
    Represents a character, can be a zombie or human
    """

    id: str
    position: Position
    is_zombie: bool
    health: int
    is_stunned: bool

    def deserialize(blob: object) -> "Character":
        try:
            assert_blob_has_key_of_type(blob, "id", str)
            assert_blob_has_key_of_type(blob, "position", dict)
            assert_blob_has_key_of_type(blob, "zombie", bool)
            assert_blob_has_key_of_type(blob, "health", int)
            assert_blob_has_key_of_type(blob, "stunned", bool)
            character = Character(
                blob["id"],
                Position.deserialize(blob["position"]),
                blob["zombie"],
                blob["health"],
                blob["stunned"],
            )
        except:
            print("Failed to validate Character json")
            raise

        return character
