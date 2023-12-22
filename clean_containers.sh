#!/bin/sh

# e.g. CONTAINER_REGISTRY=asia.gcr.io/your-project-name/gcf/asia-northeast1, chmod +x clean_containers.sh, csh delete_images.sh
CONTAINER_REGISTRY='us.gcr.io/findamare/gcf/us-central1'
IMAGE_LIST=`gcloud container images list --repository=$CONTAINER_REGISTRY | awk 'NR!=1'`

for line in $IMAGE_LIST; do
  gcloud container images delete "$line/worker" --quiet & gcloud container images delete "$line/cache" --quiet &
done

wait