docker run -p 7877:7687 -p 7445:7444 --name memgraph memgraph/memgraph-mage


docker exec -it memgraph mgconsole

docker run --rm -it --privileged --pid=host justincormack/nsenter1
nano /etc/sysctl.d/99-memgraph-vm-map-count.conf
vm.max_map_count=262144
sysctl -p /etc/sysctl.d/99-memgraph-vm-map-count.conf
sysctl vm.max_map_count
vm.max_map_count = 262144
