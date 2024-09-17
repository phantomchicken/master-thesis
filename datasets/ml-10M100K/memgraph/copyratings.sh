#!/bin/bash

# Copies ratings00.csv to ratings10.csv to the Docker container
CONTAINER_NAME=memgraph
SOURCE_DIR=..
DEST_DIR=/var/lib/memgraph

for i in {00..10}
do
    FILE="ratings$i.csv"
    echo "Copying $FILE to Docker container..."
    docker cp "$SOURCE_DIR/$FILE" "$CONTAINER_NAME:$DEST_DIR/$FILE"
done

echo "All files copied successfully!"
