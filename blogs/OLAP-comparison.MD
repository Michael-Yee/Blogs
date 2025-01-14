---
title: Comparing Real-Time OLAP Databases Apache Druid, ClickHouse and StarRocks
author: Michael Yee
published: True
---

# Overview

In this blog, I will attempt to provide a fair comparison of a few open-source real-time OLAP databases.

---

# Comparison Structure

Historically, batch data processing was the starndard to feed reports or dashboards with some interval of delayed.  Recently, there has been shift in the analytics world where we now want to real-time reports or dashboards.

The choice for our real-time OLAP databases depends on several factors where services such as AWS Athena (Presto) or AWS Redshift in previous discussions will not be a good fit.  Our inital requirement are as follows: 


- APi support
- Batch and real-time data ingestion
- Cloud provider agnositic 
	- on-premise deployment
- Control over Total Cost of Ownership (TCO)
- Open source
	- Database-as-a-Service (DBaaS)
		- Consultants
- Power BI compatible 
	- Analitics tool agnositic
- Performance
 	- Sub second complex queries
- Scalable
- Shallow learning curve

In my option, I have choosen the most popular oopen-source real-time OLAP databases as follow: Apache Druid v27.0.0, ClickHouse v23.9 and StarRocks v2.5.13.

# 

# Batch and real-time data ingestion
Apache Kafka - All three yes

Batch Data Sources




# Summary

Based on our observations, as described below in great detail, here’s a quick summary of the strengths and weaknesses of each system.

## Apache Druid

Highlights
Apache Druid is also designed to handle large-scale data and does a great job of ingesting from real-time and batch data sources. It has great support for data pre-processing during ingestion and also has recently launched a flexible SQL based ingestion approach. 

Needs Improvements
Apache Druid currently does not support real-time upserts, which is needed in many critical use cases. It does not support any way to push/write data in real time. It has limited indexing capabilities and no current support for any cloud based tiered storage.

## ClickHouse

Highlights
Of all the three systems, ClickHouse is the easiest to get started for new developers with the least number of components. Compared to the other two - it has a better real-time push model (although it also has some limitations). It has great data type support and very rich support for outbound connectors.

Needs Improvements
ClickHouse has poor support for pulling data from real-time sources (see below why this is important). Like Druid, indexing support is also quite limited, which hinders query performance, especially when dealing with a large amount of data. Although single node deployment is easy, running ClickHouse in distributed mode is quite complex. It has some operational limitations in terms of difficulty to scale-up/out nodes, lack of multi-tenancy, and management console. In general, scalability is one of the key challenges with ClickHouse.

## StarRocks

Highlights

Needs Improvements

# Conclusion
