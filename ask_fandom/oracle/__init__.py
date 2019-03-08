"""
Parses a given question in natural language and picks an Oracle class
"""
# allow oracles to be discovered
from .oracles import EpisodeFactOracle, PersonFactOracle, WoWGroupsMemberOracle
