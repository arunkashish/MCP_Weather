from typing import Any
import httpx
import asyncio
import json
from mcp.server.fastmcp import FastMCP

#Intialise FastMCP server
mcp=FastMCP("weather") 

#open Weather API
NWS_API_BASE="https://api.weather.gov"
USER_AGENT="weather-mcp/1.0"

# Define headers
headers = {
    "User-Agent": USER_AGENT
}

#API _ CALL
async def make_mws_request(url:str,params:dict[str,Any])->dict[str,Any]:
    """
    Make a request to the National Weather Service API
    """
    async with httpx.AsyncClient() as client:
        try:
            response=await client.get(url,headers=headers,timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise Exception(f"HTTP request error: {e}")
        except Exception as e:
            raise Exception(f"Error fetching data from {url}: {e}")
        

def format_alert_data(feature:dict) -> str:
    """
    Format alert data from the National Weather Service API
    """
    props=feature["properties"]
    return f"""
        Event: {props.get("event","Unknown")}
        Area: {props.get("areaDesc","Unknown")}
        Severity: {props.get("severity","Unknown")}
        Description: {props.get("description","Unknown")}
        Instruction: {props.get("instruction","Unknown")}
        """
    
@mcp.tool()
async def get_alerts(state:str)->str:
    """
    Get weather alerts for a given state.
    Args:
        state: Two-letter state code (e.g., "CA", "NY", "TX", "WA", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "MI", "MN", "MS", "MO", "NE", "NV", "NH", "NJ", "NM", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "WA", "WV", "WI", "WY")
    """
    url=f"{NWS_API_BASE}/alerts/active/area/{state}"
    data=await make_mws_request(url, params={})

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found"

    if not data["features"]:
        return "No active alerts for this state"

    alerts=[format_alert_data(feature) for feature in data["features"]
    ]
    return "\n\n".join(alerts)


#here we are just reading a CONFIG app , we can also use Greetinf  by searching the useage in Python-SDK
# @mcp.resource("config://app")
# def get_config() -> str:
#     """Static configuration data"""
#     return "App configuration here"


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"