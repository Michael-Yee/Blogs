---
title: Elasticsearch - Snapshot and restore
author: Michael Yee
published: True
---


# Snapshot and restore

A snapshot is a backup of a running Elasticsearch cluster. You can use snapshots to:

- Regularly back up a cluster with no downtime
- Recover data after deletion or a hardware failure

## The snapshot workflow

Elasticsearch stores snapshots in an off-cluster storage location called a snapshot repository. Before you can take or restore snapshots, you must register a snapshot repository on the cluster. 

After you register a snapshot repository, you can use snapshot lifecycle management (SLM) to automatically take and manage snapshots. You can then restore a snapshot to recover or transfer its data.

## Snapshot contents

By default, a snapshot of a cluster contains the cluster state, all regular data streams, and all regular indices. The cluster state includes:

- Persistent cluster settings
- Index templates
- Legacy index templates
- Ingest pipelines
- ILM policies
- Feature states

Snapshots don’t contain or back up:

- Transient cluster settings
- Registered snapshot repositories
- Node configuration files
- Security configuration files


## How snapshots work

Snapshots are automatically deduplicated to save storage space and reduce network transfer costs. To back up an index, a snapshot makes a copy of the index’s segments and stores them in the snapshot repository. Since segments are immutable, the snapshot only needs to copy any new segments created since the repository’s last snapshot.

Each snapshot is also logically independent. When you delete a snapshot, Elasticsearch only deletes the segments used exclusively by that snapshot. Elasticsearch doesn’t delete segments used by other snapshots in the repository.


## Snapshot start and stop times

A snapshot doesn’t represent a cluster at a precise point in time. Instead, each snapshot includes a start and end time. The snapshot represents a view of each shard’s data at some point between these two times.

## Snapshot compatibility

To restore a snapshot to a cluster, the versions for the snapshot, cluster, and any restored indices must be compatible.

## Snapshot version compatibility

You can’t restore a snapshot to an earlier version of Elasticsearch. For example, you can’t restore a snapshot taken in 7.6.0 to a cluster running 7.5.0.

## Index compatibility

Any index you restore from a snapshot must also be compatible with the current cluster’s version. If you try to restore an index created in an incompatible version, the restore attempt will fail.

## Other backup methods

**Taking a snapshot is the only reliable and supported way to back up a cluster.**

## Repository content

**Don’t modify anything within the repository or run processes that might interfere with its contents.**


---


Reference: [Elasticsearch Snapshot and restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html#snapshot-restore) 