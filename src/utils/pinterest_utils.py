# Follow this link for initial setup: https://github.com/pinterest/pinterest-python-sdk#getting-started


# Board information can be fetched from profile page or from create/list board method here:
# https://developers.pinterest.com/docs/api/v5/#operation/boards/list


from pinterest.client import PinterestSDKClient
from pinterest.organic.boards import Board
from pinterest.organic.pins import Pin


def create_board(
    token: str, name: str, description: str, privacy: str = "PUBLIC"
) -> str:
    """
    Create a new board on Pinterest.

    Parameters:
    name (str): The name of the board.
    description (str): A description of the board.
    privacy (str): The privacy setting of the board. Default is "PUBLIC".

    Returns:
    str: The ID of the newly created board.
    """
    PinterestSDKClient.set_default_access_token(token)

    board_create = Board.create(name=name, description=description, privacy=privacy)
    print(f"Board Id: {board_create.id}, Board name: {board_create.name}")
    return board_create.id


def create_pin(
    token: str, board_id: str, title: str, description: str, image_url: str
) -> str:
    """
    Create a new pin on a specified Pinterest board.

    Parameters:
    board_id (str): The ID of the board to which the pin will be added.
    title (str): The title of the pin.
    description (str): A description of the pin.
    image_url (str): The URL of the image to be pinned.

    Returns:
    str: The ID of the newly created pin.
    """
    PinterestSDKClient.set_default_access_token(token)
    pin_create = Pin.create(
        board_id=board_id,
        title=title,
        description=description,
        media_source={
            "source_type": "image_url",
            "content_type": "image/jpeg",
            "data": "string",
            "url": image_url,
        },
    )
    print(f"Pin Id: {pin_create.id}, Pin Title: {pin_create.title}")
    return pin_create.id


USER_TOKEN = "****"


# Usage Example:
# board_id = create_board(
#     token=USER_TOKEN, name="Summer Recipes", description="My favorite summer recipes"
# )


BOARD_ID = "976155356672267511"
pin_id = create_pin(
    token=USER_TOKEN,
    board_id=BOARD_ID,
    title="My Pin",
    description="Pin Description",
    image_url="https://firebasestorage.googleapis.com/v0/b/opencreator-1699308232742.appspot.com/o/Blog%2Ftheallurecode%2Ftheallurecode_logo.PNG?alt=media&token=ee28488d-e3dc-41c0-a9ec-3dc4c3318b36",
)
