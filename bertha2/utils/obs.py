import simpleobsws

from bertha2.settings import obs_websocket_url


def create_obs_websocket_client():
    # Create an IdentificationParameters object (optional for connecting)
    parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
    # Every possible argument has been passed, but none are required. See lib code for defaults.
    return simpleobsws.WebSocketClient(url=obs_websocket_url, identification_parameters=parameters)
