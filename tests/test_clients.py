import pytest
from unittest.mock import patch
from clients.active_campaign_client import ActiveCampaignClient

@pytest.fixture
def ac_client():
    api_key = 'test_api_key'
    base_url = 'https://test.activecampaign.com'
    return ActiveCampaignClient(api_key, base_url)

@patch('clients.active_campaign_client.requests.Session.get')
def test_get_automations(mock_get, ac_client):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'automations': []}

    response = ac_client.get_automations()
    assert response == {'automations': []}
    mock_get.assert_called_once_with('https://test.activecampaign.com/api/3/automations', headers={'Accept': 'application/json', 'Api-Token': 'test_api_key'})

if __name__ == '__main__':
    pytest.main()
