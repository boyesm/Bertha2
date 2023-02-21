import asyncio

import simpleobsws

from bertha2.settings import obs_websocket_url, video_width, video_height
from bertha2.utils.logs import initialize_module_logger

logger = initialize_module_logger(__name__)


def create_obs_websocket_client():
    # Create an IdentificationParameters object (optional for connecting)
    parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
    # Every possible argument has been passed, but none are required. See lib code for defaults.
    return simpleobsws.WebSocketClient(url=obs_websocket_url, identification_parameters=parameters)


obs_ws_client = create_obs_websocket_client()


async def update_obs_source_properties(updated_source_properties):
    # This will error if OBS isn't running
    try:
        await obs_ws_client.connect()  # Make the connection to obs-websocket
        await obs_ws_client.wait_until_identified()  # Wait for the identification handshake to complete

    except Exception as e:
        logger.error("Couldn't connect to OBS, is it open?")
        return {}

    # The type of the input is "text_ft2_source_v2"
    request = simpleobsws.Request('SetInputSettings', updated_source_properties)
    response = await obs_ws_client.call(request)  # Perform the request

    if response.ok():  # Check if the request succeeded
        logger.debug(f"Request succeeded! Response data: {response.responseData}")
    else:
        logger.warning(f"There was an error setting the text in OBS")

    await obs_ws_client.disconnect()  # Disconnect from the websocket server cleanly

    return response


def obs_change_text_source_value(text_source_id, text_value: str):
    updated_source_properties = {
        'inputName': text_source_id,
        'inputSettings': {
            'text': text_value,
        }
    }

    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_source_properties(updated_source_properties))


def obs_change_video_source_value(video_source_id, video_filepath: str):
    # Use this as a reference for the different options available:
    #     https://github.com/Elektordi/obs-websocket-py/blob/e92960a475d3f1096a4ea41763cbc776b23f0a37/obswebsocket/requests.py#L1480

    updated_source_properties = {
        'inputName': video_source_id,
        'inputSettings': {
            'local_file': video_filepath,
            'width': video_width,
            'height': video_height,
        }
    }

    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_source_properties(updated_source_properties))
