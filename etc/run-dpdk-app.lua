--
-- DPDK Packet Generator Template Script
-- by Andriy Berestovskyy
--
-- Configuration: port0 -- DUT -- port1
--
-- port0 destination is port1
-- port1 destination is port0
--
-- DUT must be a bridge
--

package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"

require "Pktgen";

local ip0 = "${IP0}";
local ip1 = "${IP1}";
local netmask = "/24"
local mac0 = "${MAC0}";
local mac1 = "${MAC1}";
local pkt_size = 64;
local rate = 100;

pktgen.set_mac("0", mac0);
pktgen.set_ipaddr("0", "src", ip0..netmask);
pktgen.set_ipaddr("0", "dst", ip1);
pktgen.set("0", "rate", rate);
pktgen.set("0", "size", pkt_size);

pktgen.set_mac("1", mac1);
pktgen.set_ipaddr("1", "src", ip1..netmask);
pktgen.set_ipaddr("1", "dst", ip0);
pktgen.set("1", "rate", rate);
pktgen.set("1", "size", pkt_size);


--pktgen.page("range");

pktgen.set_range("all", "on");

pktgen.range.src_mac("0", "start", mac0);
pktgen.range.src_mac("0", "min", mac0);
pktgen.range.src_mac("0", "max", mac0);
pktgen.range.dst_mac("0", "start", mac1);
pktgen.range.dst_mac("0", "min", mac1);
pktgen.range.dst_mac("0", "max", mac1);

pktgen.range.dst_ip("0", "start", ip1);
pktgen.range.dst_ip("0", "min", ip1);
pktgen.range.dst_ip("0", "max", ip1);
pktgen.range.dst_ip("0", "inc", "0.0.0.0");
pktgen.range.src_ip("0", "start", ip0);
pktgen.range.src_ip("0", "min", ip0);
pktgen.range.src_ip("0", "max", ip0);
pktgen.range.src_ip("0", "inc", "0.0.0.0");

pktgen.range.src_mac("1", "start", mac1);
pktgen.range.src_mac("1", "min", mac1);
pktgen.range.src_mac("1", "max", mac1);
pktgen.range.dst_mac("1", "start", mac0);
pktgen.range.dst_mac("1", "min", mac0);
pktgen.range.dst_mac("1", "max", mac0);

pktgen.range.dst_ip("1", "start", ip0);
pktgen.range.dst_ip("1", "min", ip0);
pktgen.range.dst_ip("1", "max", ip0);
pktgen.range.dst_ip("1", "inc", "0.0.0.0");
pktgen.range.src_ip("1", "start", ip1);
pktgen.range.src_ip("1", "min", ip1);
pktgen.range.src_ip("1", "max", ip1);
pktgen.range.src_ip("1", "inc", "0.0.0.0");

pktgen.range.dst_port("all", "start", 1);
pktgen.range.dst_port("all", "inc", 0);
pktgen.range.dst_port("all", "min", 1);
pktgen.range.dst_port("all", "max", 768);

pktgen.range.src_port("all", "start", 1);
pktgen.range.src_port("all", "inc", 0);
pktgen.range.src_port("all", "min", 1);
pktgen.range.src_port("all", "max", 1024);

--pktgen.page("main");
