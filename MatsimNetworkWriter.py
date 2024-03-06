import numpy as np
from matsim.writers import XmlWriter
from typing import Dict, Union, Collection, TypeVar

Id = TypeVar('Id', str, int)

class NetworkWriter(XmlWriter):
    NETWORK_SCOPE = 0
    FINISHED_SCOPE = 1
    LINKS_SCOPE = 2
    NODES_SCOPE = 3

    def __init__(self, writer):
        XmlWriter.__init__(self, writer)

    def start_network(self, attributes=None):
        self._require_scope(self.NO_SCOPE)
        self._write_line('<?xml version="1.0" encoding="utf-8"?>')
        self._write_line('<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">')
        self._write_line('<network>')
        self.set_scope(self.NETWORK_SCOPE)
        self.indent += 1
        if attributes is not None:
            self.write_preamble_attributes(attributes)

    def end_network(self):
        self._require_scope(self.NETWORK_SCOPE)
        self.indent -= 1
        self._write_line('</network>')
        self.set_scope(self.FINISHED_SCOPE)


    def start_nodes(self):
        self._require_scope(self.NETWORK_SCOPE)
        self._write_line('<nodes>')
        self.set_scope(self.NODES_SCOPE)
        self.indent += 1

    def end_nodes(self):
        self._require_scope(self.NODES_SCOPE)
        self.indent -= 1
        self.set_scope(self.NETWORK_SCOPE)
        self._write_line('</nodes>')

    def add_node(self, node_id: Id, x_coord: float, y_coord: float):
        self._require_scope(self.NODES_SCOPE)
        self._write_line(f'<node id="{node_id}" x="{x_coord}" y="{y_coord}">')
        self._write_line('</node>')   

    def start_links(self):
        self._require_scope(self.NETWORK_SCOPE)
        self._write_line('<links capperiod="01:00:00" effectivecellsize="7.5" effectivelanewidth="3.75">')
        self.set_scope(self.LINKS_SCOPE)
        self.indent += 1

    def end_links(self):
        self._require_scope(self.LINKS_SCOPE)
        self.indent -= 1
        self.set_scope(self.NETWORK_SCOPE)
        self._write_line('</links>')

    def add_link(self, link_id: Id, from_node: Id, to_node: Id, length: float, freespeed: float, capacity: float, permlanes: int, oneway: bool, modes: str):
        self._require_scope(self.LINKS_SCOPE)
        self._write_line(f'<link id="{link_id}" from="{from_node}" to="{to_node}" length="{length}", freespeed="{freespeed}" capacity="{capacity}" permlanes="{permlanes}" oneway="{oneway}" modes="{modes}">')
        self._write_line('</link>')

