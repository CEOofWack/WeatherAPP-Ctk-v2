import pytest
from unittest.mock import Mock, patch, MagicMock
from displayWeather import get_city_id, get_weather_response, get_image_for_condition
from cityList import city_list


class TestGetCityId:
    """Test the get_city_id function"""

    def test_get_city_id_ottawa(self):
        """Test that Ottawa returns correct ID"""
        assert get_city_id("ottawa") == "6094817"

    def test_get_city_id_tokyo(self):
        """Test that Tokyo returns correct ID"""
        assert get_city_id("tokyo") == "1850147"

    def test_get_city_id_case_insensitive(self):
        """Test that city names are case insensitive"""
        assert get_city_id("OTTAWA") == "6094817"
        assert get_city_id("Ottawa") == "6094817"
        assert get_city_id("oTTaWa") == "6094817"

    def test_get_city_id_unknown_city(self):
        """Test that unknown city returns default Ottawa ID"""
        assert get_city_id("unknown_city") == "6094817"
        assert get_city_id("") == "6094817"
        assert get_city_id("fake_place") == "6094817"

    def test_get_city_id_all_cities(self):
        """Test all cities in city_list return their correct IDs"""
        for city_name, city_id in city_list:
            assert get_city_id(city_name) == city_id


class TestGetWeatherResponse:
    """Test the get_weather_response function"""

    @patch('displayWeather.requests.get')
    def test_get_weather_response_success(self, mock_get):
        """Test successful API response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": "data"}
        mock_get.return_value = mock_response

        response = get_weather_response("6094817", "test_api_key")

        assert response.status_code == 200
        mock_get.assert_called_once()
        assert "6094817" in mock_get.call_args[0][0]
        assert "test_api_key" in mock_get.call_args[0][0]

    @patch('displayWeather.requests.get')
    def test_get_weather_response_correct_url_format(self, mock_get):
        """Test that URL is formatted correctly"""
        mock_response = Mock()
        mock_get.return_value = mock_response

        get_weather_response("12345", "my_api_key")

        called_url = mock_get.call_args[0][0]
        assert "id=12345" in called_url
        assert "appid=my_api_key" in called_url
        assert "units=metric" in called_url
        assert called_url.startswith("http://api.openweathermap.org")

    @patch('displayWeather.requests.get')
    def test_get_weather_response_api_failure(self, mock_get):
        """Test handling of API failure"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = get_weather_response("invalid_id", "test_api")
        assert response.status_code == 404


class TestGetImageForCondition:
    """Test the get_image_for_condition function"""

    @patch('displayWeather.Image.open')
    def test_light_rain_condition(self, mock_open):
        """Test light rain returns rainy image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("light rain")
        mock_open.assert_called_once()
        assert "rainy.jpeg" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_thunder_storm_condition(self, mock_open):
        """Test thunder storm returns thunderstorm image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("thunder storm")
        assert "thunderstorm.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_clear_sky_condition(self, mock_open):
        """Test clear sky returns sunny image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("clear sky")
        assert "sunny.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_overcast_clouds_condition(self, mock_open):
        """Test overcast clouds returns cloudy image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("overcast clouds")
        assert "cloudy.jpg" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_snow_condition(self, mock_open):
        """Test snow returns snowy image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("snow")
        assert "snowy.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_haze_condition(self, mock_open):
        """Test haze returns haze image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("haze")
        assert "haze.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_case_insensitive_condition(self, mock_open):
        """Test conditions are case insensitive"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("CLEAR SKY")
        assert "sunny.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_default_condition(self, mock_open):
        """Test unknown condition returns default snowy image"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("unknown_weather")
        assert "snowy.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_none_condition(self, mock_open):
        """Test None condition returns default"""
        mock_open.return_value = MagicMock()
        get_image_for_condition(None)
        assert "snowy.png" in mock_open.call_args[0][0]

    @patch('displayWeather.Image.open')
    def test_empty_string_condition(self, mock_open):
        """Test empty string returns default"""
        mock_open.return_value = MagicMock()
        get_image_for_condition("")
        assert "snowy.png" in mock_open.call_args[0][0]