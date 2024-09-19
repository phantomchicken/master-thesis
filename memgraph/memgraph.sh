#!/bin/bash

# Check if the vm.max_map_count modification is already done
if ! docker run --rm -it --privileged --pid=host justincormack/nsenter1 bash -c "sysctl vm.max_map_count" | grep -q 'vm.max_map_count = 262144'; then
    # Use nsenter1 to modify vm.max_map_count on the host system
    docker run --rm -it --privileged --pid=host justincormack/nsenter1 bash -c "
    echo 'vm.max_map_count=262144' > /etc/sysctl.d/99-memgraph-vm-map-count.conf &&
    sysctl -p /etc/sysctl.d/99-memgraph-vm-map-count.conf &&
    sysctl vm.max_map_count
    "
else
    echo "vm.max_map_count is already set to 262144"
fi

echo 'vm.max_map_count=262144' > /etc/sysctl.d/99-memgraph-vm-map-count.conf
docker start memgraph && docker exec -it -u 0 memgraph sh
docker run --hostname=ff6706cdae81 --user=memgraph --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=PY_VERSION=3.9 --env=LD_LIBRARY_PATH=/usr/lib/memgraph/query_modules -p 7445:7444 -p 7877:7687 --restart=no --runtime=runc -d memgraph/memgraph-mage

# Check if the container is already running
if [ "$(docker ps -q -f name=memgraph)" ]; then
    echo "Memgraph container is already running."
else
    echo "Starting Memgraph container..."
    docker run -p 7877:7687 -p 7445:7444 --name memgraph -d memgraph/memgraph-mage
    # Wait for the container to start
    sleep 10
fi


# Define the dataset directory and files
DATASET_DIR="../datasets/ml-10M100K"
FILES=("movies.csv" "ratings.csv" "tags.csv" "genres.csv" "users.csv" "movie_genre_edges.csv" "ratings00.csv" "ratings01.csv" "ratings02.csv" "ratings03.csv" "ratings04.csv" "ratings05.csv" "ratings06.csv" "ratings07.csv" "ratings08.csv" "ratings09.csv" "ratings10.csv")

# Check if all files exist before proceeding
for file in "${FILES[@]}"; do
    if [[ ! -f "$DATASET_DIR/$file" ]]; then
        echo "Error: $file not found in $DATASET_DIR."
        exit 1
    fi
done

# After container is loaded, copy dataset files into the Memgraph container
for file in "${FILES[@]}"; do
    docker cp "$DATASET_DIR/$file" memgraph:/var/lib/memgraph/"$file"
done

echo "All files copied to the Memgraph container."

# Uncomment to enter the Memgraph console (optional)
# docker exec -it memgraph mgconsole
