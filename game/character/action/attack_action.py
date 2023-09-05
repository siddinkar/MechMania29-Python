from dataclasses import asdict, dataclass
from game.character.action.attack_action_type import AttackActionType
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type


@dataclass
class AttackAction:
    """
    An attack action from one character to an object
    """

    executing_character_id: str
    attacking_id: str
    type: AttackActionType

    def to_dict(self):
        dict = asdict(self)
        dict["type"] = dict["type"].value
        return dict

    def from_json(blob: object) -> "AttackAction":
        try:
            assert_blob_has_key_of_type(blob, "executingCharacterId", str)
            assert_blob_has_key_of_type(blob, "attackingId", str)
            assert_blob_has_key_of_type(blob, "type", str)
            assert any(
                blob["type"] == item.value for item in AttackActionType
            ), "Invalid attack action type"

            action = AttackAction(
                blob["executingCharacterId"],
                blob["attackingId"],
                AttackActionType[blob["type"]],
            )
        except:
            print("Failed to validate MoveAction json")
            raise

        return action
