from pywink.devices.light_bulb import WinkLightBulb


class WinkLightGroup(WinkLightBulb):
    """
    Represents a Wink light group.
    """

    def state(self):
        """
        Groups states is determined based on a combination of all devices states
        """
        return bool(self.state_true_count() != 0)

    def reading_aggregation(self):
        return self.json_state.get("reading_aggregation")

    def state_true_count(self):
        return self.reading_aggregation().get("powered").get("true_count")

    def available(self):
        count = self.reading_aggregation().get("connection").get("true_count")
        if count > 0:
            return True
        return False

    def brightness(self):
        return self.reading_aggregation().get("brightness").get("average")

    def color_model(self):
        return self.reading_aggregation().get("color_model").get("mode")

    def color_temperature_kelvin(self):
        """
        Color temperature, in degrees Kelvin.
        Eg: "Daylight" light bulbs are 4600K
        :rtype: int
        """
        return self.reading_aggregation().get("color_temperature").get("average")

    def color_hue(self):
        """
        Color hue from 0 to 1.0
        """
        return self.reading_aggregation().get("hue").get("average")

    def color_saturation(self):
        """
        Color saturation from 0 to 1.0
        :return:
        """
        return self.reading_aggregation().get("saturation").get("average")

    def supports_hue_saturation(self):
        if self.reading_aggregation().get("hue") is not None:
            return True
        return False

    def supports_temperature(self):
        if self.reading_aggregation().get("color_temperature") is not None:
            return True
        return False
