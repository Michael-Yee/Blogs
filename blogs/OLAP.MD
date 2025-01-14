---
title: How do you choose the right Online Analytical Processing (OLAP) database?
author: Michael Yee
published: True
---

# Overview

In this blog, I will explore key factors in choosing a Online Analytical Processing (OLAP) database

---

## What is a Real-time OLAP databases?

A Real-time OLAP databases is designed to then handle data storage, processing and analysis events or data streams as they occur in real-time. Real-time OLAP databases are optimized for low-latency query performance, high-throughput data ingestion, compute-efficient processing and handling rapidly changing data. 

## How do I choose the right database for a real-time applications?

When you choose a real-time OLAP database, the following are several factors that must be considered:

- Analytics queries: Real-time OLAP databases must provide robust query capabilities within milliseconds, including support for advanced analytical functions, complex joins and aggregations.
- Cost: Control over total cost of ownership
- Data ingestion and processing: Real-time OLAP databases are designed to ingest and and process events as they occur in real time.
- Learning curve: Real-time OLAP databases that should be easy to set up and maintain which simplifies the development and deployment process, reducing the time and resources required to get an application up and running. Furthermore, a streamlined maintenance process ensures that the database remains performant, reliable, and up-to-date with minimal effort, allowing developers to focus on improving application features and functionality rather than addressing database-related issues.
- Scalability: Real-time OLAP databases must handle growing exceptionally high data volumes and query loads without sacrificing performance, by supporting horizontal scaling through sharding, partitioning, or other means.
- SQL: Real-time OLAP databases should support SQL so that they can more easily integrate with various tools, simplify query building and provide an accessible way for team members to interact with and analyze data.

## Which databases should I used for Real-Time Analytics?

### Amazon Redshift

Amazon Redshift uses SQL to analyze structured and semi-structured data across data warehouses, operational databases and data lakes, using AWS-designed hardware and machine learning to deliver the best price performance at any scale.

Amazon Redshift’s scalable, high performance and easy integration make it an excellent tool for handling large-scale data analytics and warehousing with the AWS ecosystem.

Cons:
- Concurrency
- Data duplication
- Infrastruture management
- Indexing

Pros:
- Connectors, tools and integrations
- Cost
- Performance
- Security
- Scalability
- Support

### PostgreSQL 

PostgreSQL is considered to be more of an Online Transaction Processing (OLTP) database, as it is optimized for handling a high volume of concurrent transactions, such as insert, update, and delete operations. However, it also has some Online Analytical Processing (OLAP) capabilities, such as support for complex queries and advanced data warehousing features.

If you are just getting started with some analytics or a proof of concept, where scalability is not a primary concern, PostgreSQL is a great solution. 

Cons:
- API support: Lack of built-in API support
- Performance: Not optimzied for analytical queries over many many rows of data 
- Scalability: Not designed for horizontal scalability

Pros

- Cost: PostgreSQL is open-source or a low costing SaaS 
- Learning curve: Most developers are familar with PostgreSQL and its SQL dialect is well documented and supported
- OLTP:  Supports deletes and updates which simplifies dedplication

### Snowflake 

Snowflake is a cloud-based data platform solution with a next generation SQL query engine.  

Snowflake is one of the more popular production ready choices which meets requirements for business intelligence and analytics, data ingestion, data sharing and collaboration and machine learning and a lot of other important business requirements.

Cons:
- Cost
- Community Support
- Data streaming 
- On-premises

Pros:
- Connectors, tools and integrations
- Cusomter Support
- Data caching
- Data protection
- Documentation
- Infrastruture management
- Learning curve
- Micro partitions
- Security protection
- Performance
- Scalability


# Final thoughts

To be effective in handling real-time complex analytical queries, a database must possess exceptionally high performance and scalability.

Real-time databases are the go-to choice for applications that require rapid data processing, analysis and decision-making based on the most recent data generated. 

# Next steps

Comparing Real-Time OLAP Databases Apache Druid, AWS Athena (Presto), AWS Redshft, ClickHouse and StarRocks
