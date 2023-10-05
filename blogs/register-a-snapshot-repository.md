---
title: Elasticsearch - Register a snapshot repository
author: Michael Yee
published: True
---


# Register a snapshot repository

This guide shows you how to register a snapshot repository. A snapshot repository is an off-cluster storage location for your snapshots. You must register a repository before you can take or restore snapshots.

In this guide, you’ll learn how to:

- Register a snapshot repository
- Verify that a repository is functional
- Clean up a repository to remove unneeded files

## Manage snapshot repositories

You can register and manage snapshot repositories in two ways:

- Kibana’s Snapshot and Restore feature
- Elasticsearch’s snapshot repository management APIs

To manage repositories in Kibana, go to the main menu and click **Stack Management > Snapshot and Restore > Repositories**. To register a snapshot repository, click **Register repository**.

You can also register a repository using the Create snapshot repository API.

```
PUT /_snapshot/my_repository
{
  "type": "fs",
  "settings": {
    "location": "my_backup_location"
  }
}
```

## Verify a repository

When you register a snapshot repository, Elasticsearch automatically verifies that the repository is available and functional on all master and data nodes.

If wanted, you can manually run the repository verification check. To verify a repository in Kibana, go to the Repositories list page and click the name of a repository. Then click Verify repository. You can also use the verify snapshot repository API.

```POST _snapshot/my_unverified_backup/_verify```

## Clean up a repository

Repositories can over time accumulate data that is not referenced by any existing snapshot. This is a result of the data safety guarantees the snapshot functionality provides in failure scenarios during snapshot creation and the decentralized nature of the snapshot creation process. This unreferenced data does in no way negatively impact the performance or safety of a snapshot repository but leads to higher than necessary storage use. To remove this unreferenced data, you can run a cleanup operation on the repository. This will trigger a complete accounting of the repository’s contents and delete any unreferenced data.

To run the repository cleanup operation in Kibana, go to the Repositories list page and click the name of a repository. Then click Clean up repository.

You can also use the clean up snapshot repository API.

```POST _snapshot/my_repository/_cleanup```

## Back up a repository

You may wish to make an independent backup of your repository, for instance so that you have an archive copy of its contents that you can use to recreate the repository in its current state at a later date.

You must ensure that Elasticsearch does not write to the repository while you are taking the backup of its contents. You can do this by unregistering it, or registering it with readonly: true, on all your clusters. If Elasticsearch writes any data to the repository during the backup then the contents of the backup may not be consistent and it may not be possible to recover any data from it in future.

Alternatively, if your repository supports it, you may take an atomic snapshot of the underlying filesystem and then take a backup of this filesystem snapshot. It is very important that the filesystem snapshot is taken atomically.

You cannot use filesystem snapshots of individual nodes as a backup mechanism. You must use the Elasticsearch snapshot and restore feature to copy the cluster contents to a separate repository. Then, if desired, you can take a filesystem snapshot of this repository.

When restoring a repository from a backup, you must not register the repository with Elasticsearch until the repository contents are fully restored. If you alter the contents of a repository while it is registered with Elasticsearch then the repository may become unreadable or may silently lose some of its contents.


---

Reference: [Register a snapshot repository](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#self-managed-repo-types) 
