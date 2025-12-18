import numpy as np
from mcp.server.fastmcp import FastMCP

import sys
import os

# 1. Get the absolute path of the directory where this script (afm_server.py) lives
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Point to the AFM_github folder which contains the DTMicroscope package
github_path = os.path.join(current_script_dir, "AFM_github")

# 3. Add it to the front of the path
if github_path not in sys.path:
    sys.path.insert(0, github_path)

# 4. Now the import will work perfectly
from DTMicroscope.base.afm import AFM_Microscope

# Initialize FastMCP server
mcp = FastMCP("AFM_mcp")

# Global instance of the microscope wrapper
# We initialize it outside the tools so it persists across calls
class MicroState:
    def __init__(self):
        self.microscope = None

state = MicroState()

@mcp.tool()
def initialize_microscope(type: str = "AFM", data_path: str = "AFM_github/data/AFM/BEPS_PTO_50x50.h5") -> str:
    """
    Initializes the digital twin microscope.
    Supported types: 'AFM', 'STEM', 'dummy'.
    """
    if type == "AFM":
        state.microscope = AFM_Microscope(data_path=data_path)
    # Add other types as needed
    return f"Microscope {type} initialized with data: {data_path}"

@mcp.tool()
def get_scan_area() -> dict:
    """Returns the physical boundaries (x_min, x_max, y_min, y_max) of the sample."""
    if not state.microscope:
        return {"error": "Microscope not initialized"}
    
    return {
        "x_range": [state.microscope.x_min, state.microscope.x_max],
        "y_range": [state.microscope.y_min, state.microscope.y_max],
        "current_pos": [state.microscope.x, state.microscope.y]
    }

@mcp.tool()
def perform_full_scan(channels: list = None, direction: str = 'horizontal') -> dict:
    """
    Performs a full scan of the sample.
    Returns a dict containing the array data as a list, its shape, and dtype.
    """
    if not state.microscope:
        return {"error": "Microscope not initialized"}
    
    data = state.microscope.get_scan(channels=channels, direction=direction)
    
    # Serialize for JSON transport
    return {
        "data": data.tolist(),
        "shape": data.shape,
        "dtype": str(data.dtype)
    }

@mcp.tool()
def scan_line(direction: str, coordinate: float, channels: list = None) -> dict:
    """
    Scans a single line at a specific x or y coordinate.
    coordinate: the fixed position for the axis perpendicular to scan direction.
    """
    if not state.microscope:
        return {"error": "Microscope not initialized"}
    
    line = state.microscope.scan_individual_line(direction=direction, coord=coordinate, channels=channels)
    return {
        "line_data": line.tolist(),
        "shape": line.shape
    }

@mcp.tool()
def move_tip(x: float, y: float) -> str:
    """Moves the microscope tip to a specific (x, y) location."""
    if not state.microscope:
        return "Error: Initialize first"
    
    state.microscope.go_to(x, y)
    return f"Tip moved to x={x}, y={y}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
