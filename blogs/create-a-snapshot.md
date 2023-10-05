---
title: Elasticsearch - Create a snapshot
author: Michael Yee
published: True
---


# Create a snapshot

This guide shows you how to take snapshots of a running cluster. You can later restore a snapshot to recover or transfer its data.

In this guide, you’ll learn how to:

- Automate snapshot creation and retention with snapshot lifecycle management (SLM)

The guide also provides tips for creating dedicated cluster state snapshots and taking snapshots at different time intervals.

# Automate snapshots with SLM

Snapshot lifecycle management (SLM) is the easiest way to regularly back up a cluster. An SLM policy automatically takes snapshots on a preset schedule. The policy can also delete snapshots based on retention rules you define.

TIP: Elasticsearch Service deployments automatically include the cloud-snapshot-policy SLM policy. Elasticsearch Service uses this policy to take periodic snapshots of your cluster. 

## Create an SLM policy

To manage SLM in Kibana, go to the main menu and click **Stack Management > Snapshot and Restore > Policies**. To create a policy, click Create policy.

You can also manage SLM using the SLM APIs. To create a policy, use the create SLM policy API.

The following request creates a policy that backs up the cluster state, all data streams, and all indices daily at 1:30 a.m. UTC.

```
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 1 * * ?",
  "name": "<nightly-snap-{now/d}>", 
  "repository": "my_repository",    
  "config": {
    "indices": "*",                 
    "include_global_state": true    
  },
  "retention": {                    
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

## SLM retention

SLM snapshot retention is a cluster-level task that runs separately from a policy’s snapshot schedule. To control when the SLM retention task runs, configure the slm.retention_schedule cluster setting.

```
PUT _cluster/settings
{
  "persistent" : {
    "slm.retention_schedule" : "0 30 1 * * ?"
  }
}
```

## Back up configuration files

If you run Elasticsearch on your own hardware, we recommend that, in addition to backups, you take regular backups of the files in each node’s $ES_PATH_CONF directory using the file backup software of your choice. Snapshots don’t back up these files. Also note that these files will differ on each node, so each node’s files should be backed up individually.

The elasticsearch.keystore, TLS keys, and SAML, OIDC, and Kerberos realms private key files contain sensitive information. Consider encrypting your backups of these files.

## Back up a specific feature state

By default, a snapshot that includes the cluster state also includes all feature states. Similarly, a snapshot that excludes the cluster state excludes all feature states by default.

You can also configure a snapshot to only include specific feature states, regardless of the cluster state.

To get a list of available features, use the get features API.

```
GET _features
```

To include a specific feature state in a snapshot, specify the feature name in the feature_states array.

For example, the following SLM policy only includes feature states for the Kibana and Elasticsearch security features in its snapshots.

```
PUT _slm/policy/nightly-snapshots
{
  "schedule": "0 30 2 * * ?",
  "name": "<nightly-snap-{now/d}>",
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true,
    "feature_states": [
      "kibana",
      "security"
    ]
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 5,
    "max_count": 50
  }
}
```

Any index or data stream that’s part of the feature state will display in a snapshot’s contents. For example, if you back up the security feature state, the security-* system indices display in the get snapshot API's response under both indices and feature_states.

## Create snapshots at different time interval

If you only use a single SLM policy, it can be difficult to take frequent snapshots and retain snapshots with longer time intervals.

For example, a policy that takes snapshots every 30 minutes with a maximum of 100 snapshots will only keep snapshots for approximately two days. While this setup is great for backing up recent changes, it doesn’t let you restore data from a previous week or month.

To fix this, you can create multiple SLM policies with the same snapshot repository that run on different schedules. Since a policy’s retention rules only apply to its snapshots, a policy won’t delete a snapshot created by another policy.

For example, the following SLM policy takes hourly snapshots with a maximum of 24 snapshots. The policy keeps its snapshots for one day.

```
PUT _slm/policy/hourly-snapshots
{
  "name": "<hourly-snapshot-{now/d}>",
  "schedule": "0 0 * * * ?",
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "1d",
    "min_count": 1,
    "max_count": 24
  }
}
```
 
The following policy takes nightly snapshots in the same snapshot repository. The policy keeps its snapshots for one month.

```
PUT _slm/policy/daily-snapshots
{
  "name": "<daily-snapshot-{now/d}>",
  "schedule": "0 45 23 * * ?",          
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 1,
    "max_count": 31
  }
}
```

The following policy creates monthly snapshots in the same repository. The policy keeps its snapshots for one year.

```
PUT _slm/policy/monthly-snapshots
{
  "name": "<monthly-snapshot-{now/d}>",
  "schedule": "0 56 23 1 * ?",            
  "repository": "my_repository",
  "config": {
    "indices": "*",
    "include_global_state": true
  },
  "retention": {
    "expire_after": "366d",
    "min_count": 1,
    "max_count": 12
  }
}
```

---

Reference: [Create a snapshot](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html#automate-snapshots-slm) 
