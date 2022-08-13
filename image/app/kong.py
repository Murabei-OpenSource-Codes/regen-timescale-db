"""Kong API to register reload-db."""
import requests


def register_reload_db(api_gateway_url: str, service_name: str,
                       service_url: str, reload_route: str):
    """
    Register reaload API to Kong.

    Args:
        api_gateway_url [str]: Host to kong api interface.
        service_name [str]: Service name.
        service_url [str]: Service url.
        reload_route [str]: Route to reload database.
    """
    # Creating a service for kong gateway.
    template_service = "{api_gateway_url}services/reload-db--{service_name}/"
    temp_service_url = template_service.format(
        api_gateway_url=api_gateway_url, service_name=service_name)
    payload = {
        'name': service_name, 'url': service_url}

    response = requests.put(
        temp_service_url, json=payload)
    response.raise_for_status()
    kong_service = response.json()

    #
    routes_url_template = "{api_gateway_url}routes/{route_name}"
    response = requests.put(
        routes_url_template.format(
            api_gateway_url=api_gateway_url,
            route_name="reload-db--" + service_name
        ),
        json={
            "paths": [reload_route],
            "strip_path": False,
            "service": {"id": kong_service["id"]}})
    response.raise_for_status()
    return True
