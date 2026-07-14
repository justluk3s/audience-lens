# Audience-Lense Design Document

Audience-Lense is an AI-powered audience intelligence platform designed to analyze audience discussions around online content.

The project aims to extract comments from social media platforms, organize them into a structured database, and provide increasingly advanced analytical capabilities, ranging from descriptive statistics to semantic search and natural language interaction.

The first supported platform will be YouTube due to its well-documented public API. The architecture, however, will be platform-agnostic so that additional connectors for Instagram, TikTok, Facebook, Reddit, X, and other platforms can be integrated in the future.

---
# Problem Statement

Content creators often receive thousands of comments containing valuable information.

Unfortunately, existing analytics platforms mainly provide quantitative metrics such as:
- Views.
- Likes.
- Watch time.
- Engagement.

They rarely answer qualitative questions such as:
- What are people actually talking about?
- What are the most common criticisms?
- Which topics generated the most discussion?
- How did the discussion evolve over time?
- What changed after a particular event?

Audience-Lense aims to transform large collections of comments into structured knowledge.

---
# Project Goals

The project should enable users to:
- Collect comments from content published on supported platforms.
- Store comments and related metadata in a normalized local database.
- Compute descriptive statistics.
- Visualize discussion trends over time.
- Perform semantic search across comments.
- Automatically identify and group discussion topics.
- Query the dataset using natural language.

---
# Minimum Viable Product

The initial version intentionally focuses on a limited scope.

The MVP must:
- Accept a YouTube video URL.
- Retrieve the corresponding video metadata.
- Download all available comments and replies.
- Store the collected data locally.
- Compute basic descriptive statistics.
- Generate a simple textual report.

The MVP will not include:
- Large language models.
- Embeddings.
- Topic modeling.
- Clustering.
- Dashboards.
- Multi-platform support.

These features will be introduced incrementally in future versions.

---

# Functional Requirements

## Video Collection

The system shall:
- Accept a YouTube video URL.
- Retrieve video metadata.
- Download all available comments.
- Download comment replies.

## Local Storage

The system shall store:
- Video metadata.
- Comments.
- Replies.
- Authors.
- Publication and update timestamps.
- Like counts.

## Basic Analytics

The system shall compute:
- Total number of comments.
- Total number of replies.
- Total number of likes.
- Comments per day.
- Comments per hour.
- First published comment.
- Most recently published comment.
- Average number of comments per day.
- Comment activity over time.

---
# Non-Functional Requirements

- The project shall be written in Python.
- The system shall follow a modular architecture.
- Components shall be easy to extend or replace.
- The architecture shall remain platform-agnostic.
- Data collection and analysis shall work locally.
- Components shall be easy to test.
- Analyses shall be reproducible.

---
# Design Principles

The project follows these architectural principles:
- Separation of concerns.
- Incremental development.
- Platform-agnostic architecture.
- Modular and extensible components.
- Data-first design.
- Artificial intelligence as an enhancement, not a dependency.

The system should remain useful without embeddings or large language models. AI capabilities will be introduced as additional analytical layers built on top of a reliable data collection, storage, and analytics pipeline.