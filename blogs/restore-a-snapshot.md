---
title: Elasticsearch - Restore a snapshot
author: Michael Yee
published: True
---


# Restore a snapshot

This guide shows you how to restore a snapshot. Snapshots are a convenient way to store a copy of your data outside of a cluster. You can restore a snapshot to recover indices and data streams after deletion or a hardware failure. You can also use snapshots to transfer data between clusters.

In this guide, you’ll learn how to:

- Get a list of available snapshots
- Restore an index or data stream from a snapshot
- Restore a feature state
- Monitor the restore operation
- Cancel an ongoing restore

## Prerequisite

- You can only restore a snapshot to a running cluster with an elected master node. The snapshot’s repository must be registered and available to the cluster.
- The snapshot and cluster versions must be compatible. See [Snapshot compatibility](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html#snapshot-restore-version-compatibility).

## Considerations

When restoring data from a snapshot, keep the following in mind:

- You can only restore an existing index if it’s [closed](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-close.html) and the index in the snapshot has the same number of primary shards.


## Get a list of available snapshots

To view a list of available snapshots in Kibana, go to the main menu and click **Stack Management > Snapshot and Restore**.

You can also use the get repository API and the get snapshot API to find snapshots that are available to restore. First, use the get repository API to fetch a list of registered snapshot repositories.

```
GET _snapshot
```
 
Then use the get snapshot API to get a list of snapshots in a specific repository. This also returns each snapshot’s contents.

```
GET _snapshot/my_repository/*?verbose=false
```
 
## Restore an index

You can restore a snapshot using Kibana’s **Snapshot and Restore** feature or the restore snapshot API.

By default, a restore request attempts to restore all regular indices and regular data streams in a snapshot. In most cases, you only need to restore a specific index or data stream from a snapshot. However, you can’t restore an existing open index.

If you’re restoring data to a pre-existing cluster, use one of the following methods to avoid conflicts with existing indices and data streams:

- [Delete and restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html#delete-restore)
- [Rename on restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html#rename-on-restore)

## Delete and restore

The simplest way to avoid conflicts is to delete an existing index or data stream before restoring it. To prevent the accidental re-creation of the index or data stream, we recommend you temporarily stop all indexing until the restore operation is complete.

WARNING: If the action.destructive_requires_name cluster setting is false, don’t use the delete index API to target the * or .* wildcard pattern. If you use Elasticsearch’s security features, this will delete system indices required for authentication. Instead, target the *,-.* wildcard pattern to exclude these system indices and other index names that begin with a dot (.).

```
# Delete an index
DELETE my-index

# Delete a data stream
DELETE _data_stream/logs-my_app-default
```
 
In the restore request, explicitly specify any indices and data streams to restore.

```
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default"
}
```

# Rename on restore

If you want to avoid deleting existing data, you can instead rename the indices and data streams you restore. You typically use this method to compare existing data to historical data from a snapshot. For example, you can use this method to review documents after an accidental update or deletion.

Before you start, ensure the cluster has enough capacity for both the existing and restored data.

The following restore snapshot API request prepends restored- to the name of any restored index or data stream.

```
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default",
  "rename_pattern": "(.+)",
  "rename_replacement": "restored-$1"
}
```
 
If the rename options produce two or more indices or data streams with the same name, the restore operation fails.

If you rename a data stream, its backing indices are also renamed. For example, if you rename the logs-my_app-default data stream to restored-logs-my_app-default, the backing index .ds-logs-my_app-default-2099.03.09-000005 is renamed to .ds-restored-logs-my_app-default-2099.03.09-000005.

When the restore operation is complete, you can compare the original and restored data. If you no longer need an original index or data stream, you can delete it and use a reindex to rename the restored one.

```
# Delete the original index
DELETE my-index

# Reindex the restored index to rename it
POST _reindex
{
  "source": {
    "index": "restored-my-index"
  },
  "dest": {
    "index": "my-index"
  }
}

# Delete the original data stream
DELETE _data_stream/logs-my_app-default

# Reindex the restored data stream to rename it
POST _reindex
{
  "source": {
    "index": "restored-logs-my_app-default"
  },
  "dest": {
    "index": "logs-my_app-default",
    "op_type": "create"
  }
}
```
 
## Restore a feature state

You can restore a feature state to recover system indices, system data streams, and other configuration data for a feature from a snapshot.

If you restore a snapshot’s cluster state, the operation restores all feature states in the snapshot by default. Similarly, if you don’t restore a snapshot’s cluster state, the operation doesn’t restore any feature states by default. You can also choose to restore only specific feature states from a snapshot, regardless of the cluster state.

To view a snapshot’s feature states, use the get snapshot API.

```
GET _snapshot/my_repository/my_snapshot_2099.05.06
```
 
The response’s feature_states property contains a list of features in the snapshot as well as each feature’s indices.

To restore a specific feature state from the snapshot, specify the feature_name from the response in the restore snapshot API’s feature_states parameter.

NOTE: When you restore a feature state, Elasticsearch closes and overwrites the feature’s existing indices.

WARNING: Restoring the security feature state overwrites system indices used for authentication. If you use Elasticsearch Service, ensure you have access to the Elasticsearch Service Console before restoring the security feature state. If you run Elasticsearch on your own hardware, create a superuser in the file realm to ensure you’ll still be able to access your cluster.

```
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "feature_states": [ "geoip" ],
  "include_global_state": false, # Exclude the cluster state from the restore operation.
  "indices": "-*" # Exclude the other indices and data streams in the snapshot from the restore operation.
}
``` 

## Monitor a restore

The restore operation uses the shard recovery process to restore an index’s primary shards from a snapshot. While the restore operation recovers primary shards, the cluster will have a yellow health status.

After all primary shards are recovered, the replication process creates and distributes replicas across eligible data nodes. When replication is complete, the cluster health status typically becomes green.

Once you start a restore in Kibana, you’re navigated to the **Restore Status** page. You can use this page to track the current state for each shard in the snapshot.

You can also monitor snapshot recover using Elasticsearch APIs. To monitor the cluster health status, use the cluster health API.

```
GET _cluster/health
```
 
To get detailed information about ongoing shard recoveries, use the index recovery API.

```
GET my-index/_recovery
```
 
To view any unassigned shards, use the cat shards API.

```
GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state
```
 
Unassigned shards have a state of UNASSIGNED. The prirep value is p for primary shards and r for replicas. The unassigned.reason describes why the shard remains unassigned.

To get a more in-depth explanation of an unassigned shard’s allocation status, use the cluster allocation explanation API.

```
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 0,
  "primary": false,
  "current_node": "my-node"
}
```
 
## Cancel a restore

You can delete an index or data stream to cancel its ongoing restore. This also deletes any existing data in the cluster for the index or data stream. Deleting an index or data stream doesn’t affect the snapshot or its data.

```
# Delete an index
DELETE my-index

# Delete a data stream
DELETE _data_stream/logs-my_app-default
```

## Restore to a different cluster

Elasticsearch Service can help you restore snapshots from other deployments. See Restore across clusters.

Snapshots aren’t tied to a particular cluster or a cluster name. You can create a snapshot in one cluster and restore it in another compatible cluster. Any data stream or index you restore from a snapshot must also be compatible with the current cluster’s version. The topology of the clusters doesn’t need to match.

To restore a snapshot, its repository must be registered and available to the new cluster. If the original cluster still has write access to the repository, register the repository as read-only. This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents Elasticsearch from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.

Before you start a restore operation, ensure the new cluster has enough capacity for any data streams or indices you want to restore. If the new cluster has a smaller capacity, you can:

Add nodes or upgrade your hardware to increase capacity.
Restore fewer indices and data streams.
Reduce the number of replicas for restored indices.

For example, the following restore snapshot API request uses the index_settings option to set index.number_of_replicas to 1.

```
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default",
  "index_settings": {
    "index.number_of_replicas": 1
  }
}
```
 
If indices or backing indices in the original cluster were assigned to particular nodes using shard allocation filtering, the same rules will be enforced in the new cluster. If the new cluster does not contain nodes with appropriate attributes that a restored index can be allocated on, the index will not be successfully restored unless these index allocation settings are changed during the restore operation.

The restore operation also checks that restored persistent settings are compatible with the current cluster to avoid accidentally restoring incompatible settings. If you need to restore a snapshot with incompatible persistent settings, try restoring it without the global cluster state.

Troubleshoot restore errorsedit
Here’s how to resolve common errors returned by restore requests.

Cannot restore index [<index>] because an open index with same name already exists in the clusteredit
You can’t restore an open index that already exists. To resolve this error, try one of the methods in Restore an index or data stream.

Cannot restore index [<index>] with [x] shards from a snapshot of index [<snapshot-index>] with [y] shardsedit
You can only restore an existing index if it’s closed and the index in the snapshot has the same number of primary shards. This error indicates the index in the snapshot has a different number of primary shards.

To resolve this error, try one of the methods in Restore an index or data stream.


---


Reference: [Restore a snapshot](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) 
