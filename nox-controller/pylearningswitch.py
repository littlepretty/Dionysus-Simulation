# Author: YJQ
# This app functions as the control loggeric of an L2 learning switch for
# all switches in the network


from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.packet_utils import mac_to_str, mac_to_int

import logging
logger = logging.getLogger('nox.coreapps.examples.tutorial.pylearningswitch')

CACHE_TIMEOUT = 10

class pylearningswitch(Component):
	"""docstring for pylearningswitch"""

	def __init__(self, ctxt):
		# super(pylearningswitch, self).__init__()

		Component.__init__(self, ctxt)
		self.mac_to_port = {} # Key: mac addr, Val: port number

	def learn_and_forward(self, dpid, inport, packet, buf, bufid):
		
		# learn mac on incoming port from src
		src_mac = mac_to_str(packet.src)
		dst_mac = mac_to_str(packet.dst)
		if self.mac_to_port.has_key(src_mac):
			# print update msg
			old_outport = self.mac_to_port[src_mac]
			if old_outport != inport:
				logger.info('MAC ' + src_mac + ' has moved from %d to %d', old_outport, inport)
			else:
				logger.info('MAC ' + src_mac + ' remained on %d', old_outport)
		else:
			logger.info('learned MAC ' + src_mac + ' on %d port %d', dpid, inport)
		
		self.mac_to_port[src_mac] = inport

		# try find a outport for dst
		if self.mac_to_port.has_key(dst_mac):

			outport = self.mac_to_port[dst_mac]
			if outport == inport:
				self.send_openflow(dpid, bufid, buf, openflow.OFPP_FLOOD, inport)
				logger.error('*** warning *** learned port == inport, flood packet')
			else:
				logger.info('install flow for ' + str(packet))
				flow = extract_flow(packet)
				flow[core.IN_PORT] = inport
				actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
				self.install_datapath_flow(dpid, flow, CACHE_TIMEOUT, openflow.OFP_FLOW_PERMANENT, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
		else:
			logger.info('*** warning *** no learned, flood packet')
			self.send_openflow(dpid, bufid, buf, openflow.OFPP_FLOOD, inport)

	def packet_in_callback(self, dpid, inport, reason, len, bufid, packet):
		"""packet-in handler"""
		if not packet.parsed:
			logger.info('ignoring incomplete packet')
		else:
			self.learn_and_forward(dpid, inport, packet, packet.arr, bufid)

		return CONTINUE

	def install(self):
		self.register_for_packet_in(self.packet_in_callback)

	def getInterface(self):
		return str(pylearningswitch)

def getFactory():

	class Factory:
		def instance(self, ctxt):
			return pylearningswitch(ctxt)

	return Factory()






		