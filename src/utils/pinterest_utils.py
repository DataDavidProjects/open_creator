# Follow this link for initial setup: https://github.com/pinterest/pinterest-python-sdk#getting-started


# Board information can be fetched from profile page or from create/list board method here:
# https://developers.pinterest.com/docs/api/v5/#operation/boards/list


import requests
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


# USER_TOKEN = "****"


# Usage Example:
# board_id = create_board(
#     token=USER_TOKEN, name="Summer Recipes", description="My favorite summer recipes"
# )


# BOARD_ID = "976155356672267511"
# pin_id = create_pin(
#     token=USER_TOKEN,
#     board_id=BOARD_ID,
#     title="My Pin",
#     description="Pin Description",
#     image_url="https://firebasestorage.googleapis.com/v0/b/opencreator-1699308232742.appspot.com/o/Blog%2Ftheallurecode%2Ftheallurecode_logo.PNG?alt=media&token=ee28488d-e3dc-41c0-a9ec-3dc4c3318b36",
# )


def api_endpoint(header, body, endpoint):
    response = requests.get(url=endpoint, headers=header, json=body)
    return response.json()  # Assuming the response is in JSON format


def list_pinterest_boards(access_token):
    endpoint = "https://api.pinterest.com/v5/boards"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(endpoint, headers=headers)
    return response.json()


def create_pinterest_pin(access_token, board_id, title, link, image_url, description):
    endpoint = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Only include parameters in the body if they are not None
    body = {
        "board_id": board_id,
        "media_source": {"source_type": "image_url", "url": image_url},
        "link": link,
        "title": title,
        "description": description,
    }

    response = requests.post(endpoint, headers=headers, json=body)
    return response.json()


def get_trending_keywords(region: str, trend_type: str, params: dict, access_token):
    """
    Retrieves trending keywords from Pinterest API based on specified criteria.

    This function makes a GET request to the Pinterest API's trending keywords endpoint.
    It fetches trending keywords for a given region and trend type, with additional filter
    options provided through query parameters.

    Args:
    - region (str): The geographical region for which to retrieve trending keywords.
    - trend_type (str): The type of trend for which to retrieve keywords (e.g., 'food_drink').
    - params (dict): A dictionary of query parameters to filter the results. This can include
      parameters such as interests, genders, ages, normalization options, and limit.
    - access_token (str): The access token for authenticating with the Pinterest API.

    Returns:
    - dict: A dictionary containing the JSON response from the API. This typically includes
      details about the trending keywords based on the provided criteria.
    """
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    endpoint = f"https://api.pinterest.com/v5/trends/keywords/{region}/top/{trend_type}"

    response = requests.get(url=endpoint, headers=header, params=params)

    return response.json()
