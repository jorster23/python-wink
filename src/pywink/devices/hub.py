import logging

from pywink.devices.base import WinkDevice

_LOGGER = logging.getLogger(__name__)


class WinkHub(WinkDevice):
    """
    Represents a Wink Hub.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkHub, self).__init__(device_state_as_json, api_interface)
        self._unit = None

    def unit(self):
        return self._unit

    def state(self):
        return self.available()

    def kidde_radio_code(self):
        config = self.json_state.get('configuration')
        return config.get('kidde_radio_code')

    def update_needed(self):
        return self._last_reading.get('update_needed')

    def ip_address(self):
        return self._last_reading.get('ip_address')

    def firmware_version(self):
        return self._last_reading.get('firmware_version')

    def local_control_id(self):
        return self._last_reading.get('local_control_id')

    def pairing_mode(self):
        return self._last_reading.get('pairing_mode')

    def update_firmware(self):
        return self.api_interface.update_firmware(self)

    def pair_new_device(self, pairing_mode, pairing_mode_duration=60, pairing_device_type_selector=None,
                        kidde_radio_code=None):
        """
        :param pairing_mode: a string one of ["zigbee", "zwave", "zwave_exclusion",
            "zwave_network_rediscovery", "lutron", "bluetooth", "kidde"]
        :param pairing_mode_duration: an int in seconds defaults to 60
        :param pairing_device_type_selector: a string I believe this is only for bluetooth devices.
        :param kidde_radio_code: a string of 8 1s and 0s one for each dip switch on the kidde device
            left --> right = 1 --> 8
        :return: nothing
        """
        if pairing_mode == "lutron" and pairing_mode_duration < 120:
            pairing_mode_duration = 120
        elif pairing_mode == "zwave_network_rediscovery":
            pairing_mode_duration = 0
        elif pairing_mode == "bluetooth" and pairing_device_type_selector is None:
            pairing_device_type_selector = "switchmate"

        desired_state = {"pairing_mode": pairing_mode,
                         "pairing_mode_duration": pairing_mode_duration}

        if pairing_mode == "kidde" and kidde_radio_code is not None:
            # Convert dip switch 1 and 0s to an int
            try:
                kidde_radio_code_int = int(kidde_radio_code, 2)
                desired_state = {"kidde_radio_code": kidde_radio_code_int, "pairing_mode": None}
            except (TypeError, ValueError):
                _LOGGER.error("An invalid Kidde radio code was provided. " + kidde_radio_code)

        if pairing_device_type_selector is not None:
            desired_state.update({"pairing_device_type_selector": pairing_device_type_selector})

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)
