import main
from ipaddress import IPv4Address, IPv4Network


ip_link_lines = r'''
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000\    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00 promiscuity 0 allmulti 0 minmtu 0 maxmtu 0 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000\    link/ether ee:53:e6:70:d9:15 brd ff:ff:ff:ff:ff:ff promiscuity 0 allmulti 0 minmtu 68 maxmtu 65535 addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 parentbus virtio parentdev virtio1 \    altname enp0s3\    altname enxee53e670d915
3: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000\    link/ether 06:c9:38:e0:fe:71 brd ff:ff:ff:ff:ff:ff promiscuity 0 allmulti 0 minmtu 68 maxmtu 65535 addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 parentbus virtio parentdev virtio2 \    altname enp0s4\    altname enx06c938e0fe71
4: docker_gwbridge: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default \    link/ether 02:42:e4:fa:be:fd brd ff:ff:ff:ff:ff:ff promiscuity 0 allmulti 0 minmtu 68 maxmtu 65535 \    bridge forward_delay 1500 hello_time 200 max_age 2000 ageing_time 30000 stp_state 0 priority 32768 vlan_filtering 0 vlan_protocol 802.1Q bridge_id 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd root_port 0 root_path_cost 0 topology_change 0 topology_change_detected 0 hello_timer    0.00 tcn_timer    0.00 topology_change_timer    0.00 gc_timer    0.00 fdb_n_learned 1 fdb_max_learned 0 vlan_default_pvid 1 vlan_stats_enabled 0 vlan_stats_per_port 0 group_fwd_mask 0 group_address 01:80:c2:00:00:00 mcast_snooping 1 no_linklocal_learn 0 mcast_vlan_snooping 0 mst_enabled 0 mcast_router 1 mcast_query_use_ifaddr 0 mcast_querier 0 mcast_hash_elasticity 16 mcast_hash_max 4096 mcast_last_member_count 2 mcast_startup_query_count 2 mcast_last_member_interval 100 mcast_membership_interval 26000 mcast_querier_interval 25500 mcast_query_interval 12500 mcast_query_response_interval 1000 mcast_startup_query_interval 3125 mcast_stats_enabled 0 mcast_igmp_version 2 mcast_mld_version 1 nf_call_iptables 0 nf_call_ip6tables 0 nf_call_arptables 0 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default \    link/ether 02:42:5f:f2:bc:0f brd ff:ff:ff:ff:ff:ff promiscuity 0 allmulti 0 minmtu 68 maxmtu 65535 \    bridge forward_delay 1500 hello_time 200 max_age 2000 ageing_time 30000 stp_state 0 priority 32768 vlan_filtering 0 vlan_protocol 802.1Q bridge_id 8000.2:42:5f:f2:bc:f designated_root 8000.2:42:5f:f2:bc:f root_port 0 root_path_cost 0 topology_change 0 topology_change_detected 0 hello_timer    0.00 tcn_timer    0.00 topology_change_timer    0.00 gc_timer   51.48 fdb_n_learned 0 fdb_max_learned 0 vlan_default_pvid 1 vlan_stats_enabled 0 vlan_stats_per_port 0 group_fwd_mask 0 group_address 01:80:c2:00:00:00 mcast_snooping 1 no_linklocal_learn 0 mcast_vlan_snooping 0 mst_enabled 0 mcast_router 1 mcast_query_use_ifaddr 0 mcast_querier 0 mcast_hash_elasticity 16 mcast_hash_max 4096 mcast_last_member_count 2 mcast_startup_query_count 2 mcast_last_member_interval 100 mcast_membership_interval 26000 mcast_querier_interval 25500 mcast_query_interval 12500 mcast_query_response_interval 1000 mcast_startup_query_interval 3125 mcast_stats_enabled 0 mcast_igmp_version 2 mcast_mld_version 1 nf_call_iptables 0 nf_call_ip6tables 0 nf_call_arptables 0 addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 65536 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
62: vethc9050f8@if61: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default \    link/ether aa:3d:7c:be:5f:2d brd ff:ff:ff:ff:ff:ff link-netnsid 1 promiscuity 1 allmulti 1 minmtu 68 maxmtu 65535 \    veth \    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8001 port_no 0x1 designated_port 32769 designated_cost 0 designated_bridge 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on bcast_flood on mcast_to_unicast off neigh_suppress off neigh_vlan_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off locked off mab off addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
87: veth7b712b0@if86: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default \    link/ether 96:9b:a9:b4:18:73 brd ff:ff:ff:ff:ff:ff link-netnsid 6 promiscuity 1 allmulti 1 minmtu 68 maxmtu 65535 \    veth \    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8004 port_no 0x4 designated_port 32772 designated_cost 0 designated_bridge 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on bcast_flood on mcast_to_unicast off neigh_suppress off neigh_vlan_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off locked off mab off addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
91: vethce324af@if90: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default \    link/ether 5e:f0:08:64:c5:b3 brd ff:ff:ff:ff:ff:ff link-netnsid 7 promiscuity 1 allmulti 1 minmtu 68 maxmtu 65535 \    veth \    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8005 port_no 0x5 designated_port 32773 designated_cost 0 designated_bridge 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on bcast_flood on mcast_to_unicast off neigh_suppress off neigh_vlan_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off locked off mab off addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
97: vetha26df2c@if96: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default \    link/ether b2:51:21:d4:5d:ec brd ff:ff:ff:ff:ff:ff link-netnsid 4 promiscuity 1 allmulti 1 minmtu 68 maxmtu 65535 \    veth \    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8002 port_no 0x2 designated_port 32770 designated_cost 0 designated_bridge 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on bcast_flood on mcast_to_unicast off neigh_suppress off neigh_vlan_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off locked off mab off addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
101: vethdcc6523@if100: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker_gwbridge state UP mode DEFAULT group default \    link/ether 92:f3:72:7f:f8:8f brd ff:ff:ff:ff:ff:ff link-netnsid 5 promiscuity 1 allmulti 1 minmtu 68 maxmtu 65535 \    veth \    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8003 port_no 0x3 designated_port 32771 designated_cost 0 designated_bridge 8000.2:42:e4:fa:be:fd designated_root 8000.2:42:e4:fa:be:fd hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on bcast_flood on mcast_to_unicast off neigh_suppress off neigh_vlan_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off locked off mab off addrgenmode none numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 gso_ipv4_max_size 65536 gro_ipv4_max_size 65536 
'''

def test_parse_ip_link():
    interfaces = main.parse_ip_links(ip_link_lines.splitlines())

    assert len(interfaces) == 10
    assert interfaces[1].name == 'lo'
    assert interfaces[5].state == 'DOWN'
    assert interfaces[62].veth_pair_id == 61
    assert interfaces[62].bridge_name == 'docker_gwbridge'

ip_addr_lines = r'''
1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever
1: lo    inet6 ::1/128 scope host noprefixroute \       valid_lft forever preferred_lft forever
2: ens3    inet 111.111.111.111/20 brd 111.111.111.255 scope global dynamic noprefixroute ens3\       valid_lft 62907sec preferred_lft 52107sec
2: ens3    inet6 fe80::eeee:eeee:eeee:eeee/64 scope link \       valid_lft forever preferred_lft forever
3: ens4    inet 10.106.0.3/20 brd 10.106.15.255 scope global dynamic noprefixroute ens4\       valid_lft 62909sec preferred_lft 52109sec
3: ens4    inet6 fe80::aaaa:aaaa:aaaa:aaaa/64 scope link \       valid_lft forever preferred_lft forever
4: docker_gwbridge    inet 172.19.0.1/16 brd 172.19.255.255 scope global docker_gwbridge\       valid_lft forever preferred_lft forever
4: docker_gwbridge    inet6 fe80::42:aaaa:aaaa:aaaa/64 scope link proto kernel_ll \       valid_lft forever preferred_lft forever
5: docker0    inet 10.10.0.1/24 brd 10.10.0.255 scope global docker0\       valid_lft forever preferred_lft forever
62: vethc9050f8    inet 169.254.245.179/16 brd 169.254.255.255 scope global noprefixroute vethc9050f8\       valid_lft forever preferred_lft forever
62: vethc9050f8    inet6 fe80::aaaa:aaaa:aaaa:5f2d/64 scope link \       valid_lft forever preferred_lft forever
87: veth7b712b0    inet 169.254.103.53/16 brd 169.254.255.255 scope global noprefixroute veth7b712b0\       valid_lft forever preferred_lft forever
87: veth7b712b0    inet6 fe80::aaaa:aaaa:aaaa:1873/64 scope link \       valid_lft forever preferred_lft forever
91: vethce324af    inet 169.254.114.48/16 brd 169.254.255.255 scope global noprefixroute vethce324af\       valid_lft forever preferred_lft forever
91: vethce324af    inet6 fe80::aaaa:aaaa:aaaa:c5b3/64 scope link \       valid_lft forever preferred_lft forever
97: vetha26df2c    inet 169.254.137.78/16 brd 169.254.255.255 scope global noprefixroute vetha26df2c\       valid_lft forever preferred_lft forever
97: vetha26df2c    inet6 fe80::aaaa:aaaa:aaaa:5dec/64 scope link \       valid_lft forever preferred_lft forever
101: vethdcc6523    inet 169.254.68.83/16 brd 169.254.255.255 scope global noprefixroute vethdcc6523\       valid_lft forever preferred_lft forever
101: vethdcc6523    inet6 fe80::aaaa:aaaa:aaaa:f88f/64 scope link \       valid_lft forever preferred_lft forever
'''

def test_parse_ip_addr():
    addrs = main.parse_ip_addrs(ip_addr_lines.splitlines())

    assert len(addrs) == 10
    assert addrs[1] == IPv4Address('127.0.0.1')
    assert addrs[2] == IPv4Address('111.111.111.111')
    assert addrs[4] == IPv4Address('172.19.0.1')

ip_route_lines = r'''
unicast default via 123.123.123.1 dev ens3 proto dhcp scope global src 123.123.123.123 metric 1002 mtu 1500 
unicast 10.10.0.0/24 dev docker0 proto kernel scope link src 10.10.0.1 linkdown 
unicast 10.106.0.0/20 dev ens4 proto dhcp scope link src 10.106.0.3 metric 1003 mtu 1500 
unicast 123.123.123.0/24 dev ens3 proto dhcp scope link src 123.123.123.123 metric 1002 mtu 1500 
unicast 169.254.0.0/16 dev vethc9050f8 proto boot scope link src 169.254.245.179 metric 1062 
unicast 169.254.0.0/16 dev veth7b712b0 proto boot scope link src 169.254.103.53 metric 1087 
unicast 169.254.0.0/16 dev vethce324af proto boot scope link src 169.254.114.48 metric 1091 
unicast 169.254.0.0/16 dev vetha26df2c proto boot scope link src 169.254.137.78 metric 1097 
unicast 169.254.0.0/16 dev vethdcc6523 proto boot scope link src 169.254.68.83 metric 1101 
unicast 169.254.169.254 dev ens3 proto boot scope link 
unicast 172.19.0.0/16 dev docker_gwbridge proto kernel scope link src 172.19.0.1 
'''

def test_parse_ip_route():
    routes = main.parse_ip_routes(ip_route_lines.splitlines())

    assert len(routes) == 11
    assert routes[0].gateway.address == IPv4Address('123.123.123.1')
    assert routes[0].destination == IPv4Network('0.0.0.0/0')
    assert routes[0].interface_name == 'ens3'

    assert not routes[1].gateway
    assert routes[1].destination == IPv4Network('10.10.0.0/24')
    assert routes[1].interface_name == 'docker0'

    assert routes[9].destination == IPv4Network('169.254.169.254/32')