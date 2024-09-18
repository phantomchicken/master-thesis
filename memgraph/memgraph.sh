# Step 1: Use nsenter1 to modify vm.max_map_count on the host system
docker run --rm -it --privileged --pid=host justincormack/nsenter1 bash -c "
echo 'vm.max_map_count=262144' > /etc/sysctl.d/99-memgraph-vm-map-count.conf &&
sysctl -p /etc/sysctl.d/99-memgraph-vm-map-count.conf &&
sysctl vm.max_map_count
"

# Start Memgraph container with MAGE
docker run -p 7877:7687 -p 7445:7444 --name memgraph -d memgraph/memgraph-mage

sleep 10

# After container is loaded copy dataset files into the Memgraph container
docker cp ../datasets/ml-10M100K/memgraph/moviesmemgraph.csv memgraph:/var/lib/memgraph/moviesmemgraph.csv
docker cp ../datasets/ml-10M100K/memgraph/ratingsmemgraph.csv memgraph:/var/lib/memgraph/ratingsmemgraph.csv
docker cp ../datasets/ml-10M100K/memgraph/tagsmemgraph.csv memgraph:/var/lib/memgraph/tagsmemgraph.csv
docker cp ../datasets/ml-10M100K/memgraph/genresmemgraph.csv memgraph:/var/lib/memgraph/genresmemgraph.csv
docker cp ../datasets/ml-10M100K/memgraph/usersmemgraph.csv memgraph:/var/lib/memgraph/usersmemgraph.csv
docker cp ../datasets/ml-10M100K/memgraph/movie_genre_edgesmemgraph.csv memgraph:/var/lib/memgraph/movie_genre_edgesmemgraph.csv

# docker exec -it memgraph mgconsole
