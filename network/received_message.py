from dataclasses import dataclass

from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type


@dataclass
class ReceivedMessage:
    is_zombie: bool
    type: str
    message: object

    def deserialize(blob: object) -> "ReceivedMessage":
        try:
            assert_blob_has_key_of_type(blob, "isZombie", bool)
            assert_blob_has_key_of_type(blob, "type", str)
            assert_blob_has_key_of_type(blob, "message", object)
            position = ReceivedMessage(blob["isZombie"], blob["type"], blob["message"])
        except:
            print("Failed to validate ReceivedMessage json")
            raise

        return position
