"""
Dionysus Failure Recovery Testcase
a NOX controller that 
	1. first install current rules
	2. then wait for a link failure
	3. to handle this failure, install target rules with dionysus's dependency graph and scheduling algorithms

"""

from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.packet_utils import mac_to_int, mac_to_str
from array import *
from nox.lib.util import convert_to_eaddr 

import logging
logger = logging.getLogger('nox.coreapps.examples.dionysuscontroller')
CACHE_TIMEOUT = 100

EthAddr1 = "\x00\x00\x00\x00\x00\x01"
EthAddr2 = "\x00\x00\x00\x00\x00\x02"
EthAddr3 = "\x00\x00\x00\x00\x00\x03"
EthAddr4 = "\x00\x00\x00\x00\x00\x04"
EthAddr5 = "\x00\x00\x00\x00\x00\x05"
EthAddr6 = "\x00\x00\x00\x00\x00\x06"
EthAddr7 = "\x00\x00\x00\x00\x00\x07"
EthAddr8 = "\x00\x00\x00\x00\x00\x08"
Ether_Broadcast = "\xff\xff\xff\xff\xff\xff"
Ether_Any = "\x00\x00\x00\x00\x00\x00"

h1 = array('B', EthAddr1)
h2 = array('B', EthAddr2)
h3 = array('B', EthAddr3)
h4 = array('B', EthAddr4)
h5 = array('B', EthAddr5)
h6 = array('B', EthAddr6)
h7 = array('B', EthAddr7)
h8 = array('B', EthAddr8)
broadcast = array('B', Ether_Broadcast)
anysource = array('B', Ether_Any)

IDLE_TIMEOUT = 100
HARD_TIMEOUT = 200

PORT_MAP = dict()
PORT_MAP['s1'] = dict(s8 = 1, s3 = 2, h1 = 3)
PORT_MAP['s2'] = dict(s5 = 1, s4 = 2, s7 = 3, h2 = 4)
PORT_MAP['s3'] = dict(s1 = 1, s8 = 2, s6 = 3, s4 = 4, h3 = 5)
PORT_MAP['s4'] = dict(s3 = 1, s5 = 2, s2 = 3, s7 = 4, h4 = 5)
PORT_MAP['s5'] = dict(s6 = 1, s4 = 2, s2 = 3, s7 = 4, h5 = 5)
PORT_MAP['s6'] = dict(s8 = 1, s3 = 2, s5 = 3, h6 = 4)
PORT_MAP['s7'] = dict(s8 = 1, s2 = 2, s4 = 3, s5 = 4, h7 = 5)
PORT_MAP['s8'] = dict(s1 = 1, s3 = 2, s6 = 3, s7 = 4, h8 = 5)

class dionysuscontroller(Component):
	def __init__(self, ctxt):
		Component.__init__(self, ctxt)
		self.port_map = PORT_MAP

	def install_flood_rule(self, dpid):
		flood = dict()
		flood[core.DL_DST] = broadcast
		actions = [[openflow.OFPAT_OUTPUT, openflow.OFPP_FLOOD]]
		self.install_datapath_flow(dpid, flood, IDLE_TIMEOUT, openflow.OFP_FLOW_PERMANENT, actions)

	def install_forward_entry_on_switch(self, dpid, dl_src, dl_dst, from_port, to_port):
		flow = dict()
		flow[core.DL_SRC] = dl_src
		flow[core.DL_DST] = dl_dst
		actions = [[openflow.OFPAT_OUTPUT, [0, self.port_map[from_port][to_port]]]]
		bufferid = None
		priority = 10
		inport = None
		packet = None
		self.install_datapath_flow(dpid, flow, IDLE_TIMEOUT, HARD_TIMEOUT, actions, bufferid, priority, inport, packet) 
		
	def install_rule_for_sw1(self, dpid):	
		self.install_flood_rule(dpid)

		self.install_forward_entry_on_switch(dpid, h1, h7, 's1', 's8')
		self.install_forward_entry_on_switch(dpid, h7, h1, 's1', 'h1')
		# self.install_forward_entry_on_switch(dpid, anysource, h1, 's1', 'h1')

	def install_rule_for_sw7(self, dpid):
		self.install_flood_rule(dpid)
		
		self.install_forward_entry_on_switch(dpid, h1, h7, 's7', 'h7')
		# self.install_forward_entry_on_switch(dpid, anysource, h7, 's7', 'h7')
		self.install_forward_entry_on_switch(dpid, h7, h1, 's7', 's8')		

	def install_rule_for_sw8(self, dpid):
		self.install_flood_rule(dpid)
		
		self.install_forward_entry_on_switch(dpid, h1, h7, 's8', 's7')
		self.install_forward_entry_on_switch(dpid, h7, h1, 's8', 's1')
			

	def datapath_join_callback(self, dpid, attrs):
		logger.info('switch ' + str(dpid) + ' joins in')
		str_dpid = str(dpid)
		if dpid == 1:
			self.install_rule_for_sw1(dpid)
			logger.info('Rules installed on switch ' + str(dpid))
		if dpid == 7:
			self.install_rule_for_sw7(dpid)
			logger.info('Rules installed on switch ' + str(dpid))
		if dpid == 8:
			self.install_rule_for_sw8(dpid)
			logger.info('Rules installed on switch ' + str(dpid))
			
	def packet_in_callback(self, dpid, inport, reason, len, bufid, packet):
		if not packet.parsed:
			logger.info('Ignore incomplete packets')
	
	def install(self):
		self.register_for_datapath_join(self.datapath_join_callback)

	def getInterface(self):
		return str(dionysuscontroller)

def getFactory():
	class Factory:
		def instance(self, ctxt):
			return dionysuscontroller(ctxt)

	return Factory()

