# @date: 2025/11/16
# @author: Hokyee Jau

import json
from typing import Dict

from mcp.server.fastmcp import FastMCP
mcp = FastMCP()


with open("info.json", "r", encoding='utf-8') as f:
    data = json.load(f)


def get_odor():
    return 3


def get_position():
    return 1


@mcp.tool("get_odor_type_and_position")
def get_odor_type_and_position() -> str:
    """
    Get the odor type and the odor position according to the classification paper_results
    derived by accessing the data APIs provided by the electronic nose installed at home.
    This tool returns dumped json data.
    """
    global get_odor, get_position, data

    position = data["position_list"][get_position()-1]
    odor = data["odor_list"][get_odor()-1]

    results = dict(position=position, smelling=odor)
    return json.dumps(results)


@mcp.tool("get_odor_introduction")
def get_odor_introduction(beer_type: str) -> str:
    """
    Get the introduction of the odors (beers) by the beer types ("kelly", "cass", or "terra")
    :param beer_type: should be lowercasing "kelly", "cass", or "terra"
    :return: return a dict containing the introduction extracted from Namu Wiki.
    """

    global data

    return data['odor'][beer_type.lower()]


@mcp.tool("get_e_nose_info")
def get_e_nose_info() -> Dict:
    """
    Get the information of the e-noses, including gas sensors, beer temperatures, room temperature, humidity,
    device sampling rate, the single board computers for collecting signals and the number of e-noses.
    """
    global data
    return data['electronic_nose_info']


if __name__ == '__main__':
    mcp.run(transport='stdio')