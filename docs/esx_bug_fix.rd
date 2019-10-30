_change NIC type from VMXNET3 to E1000E
_or, shutdown VM then set vmxnet3.rev.30=False under VM properties (did not work for one guy)
_or/and, ethtool -G ens192 rx-mini 0
_or/and, ethtool -K ens192 gro off; ethtool -K ens192 lro off;
_use ESXi build 6.5u1 (NOT HPE Customized Image)
_downgrade kernel to 4.4.x
