---
myst:
  html_meta:
    description: "Supported versions, lifecycle dates, and PPA details for self-hosted Landscape Server."
---

(reference-supported-versions-and-ppas)=
# Supported versions and PPAs

This document is the reference for self-hosted Landscape Server version lifecycle and package sources.

## Supported versions

The following versions of Landscape Server are currently supported. This table applies to {ref}`Quickstart <how-to-quickstart-installation>` and {ref}`Manual <how-to-manual-installation>` installations.

```{include} _includes/landscape-versions-table.md
```

**LTS releases** are published every two years, typically in April of even years. Five point releases follow, typically in February and August. Recommended for production.

**Latest stable releases** are published every six months, typically in April and October. Support ends when the next release ships. Users must upgrade to maintain support.

## PPAs

```{include} _includes/landscape-ppas-table.md
```

## Ubuntu compatibility

```{include} _includes/landscape-ubuntu-compatibility-table.md
```

Compatibility beyond the stated range is best-effort and not guaranteed.

New Landscape features are typically not backported to Landscape Client packages in older Ubuntu releases.

## Charm releases

The [Landscape Server charm](https://charmhub.io/landscape-server) follows similar release cycles to the packages. Ubuntu compatibility for the charm may differ; always check [Charmhub](https://charmhub.io/) for current channel details.

## Unsupported versions

| Version | Released | Support ended | ESM until | Ubuntu |
| ------- | -------- | ------------- | --------- | ------ |
| {ref}`reference-release-notes-25-10` | 2025-Oct | 2025-Apr | — | 22.04 LTS or 24.04 LTS |
| {ref}`reference-release-notes-25-04` | 2025-May | 2025-Oct | — | 22.04 LTS or 24.04 LTS |
| {ref}`reference-release-notes-24-10` | 2024-Nov | 2025-Apr | — | 22.04 LTS or 24.04 LTS |
| {ref}`reference-release-notes-23-10` | 2023-Oct | 2024-Apr | — | 20.04 LTS or 22.04 LTS |
| {ref}`reference-release-notes-19-10` | 2019-Oct | 2023-May-31 | — | 18.04 LTS |
| {ref}`reference-release-notes-19-01` | 2019-Jan | 2020-Jan | — | 18.04 LTS |
| {ref}`reference-release-notes-18-03` | 2018-Jun | 2019-Jun | — | 16.04 LTS or 18.04 LTS |
| {ref}`reference-release-notes-17-03` | 2017-Mar | 2019-Mar | — | 16.04 LTS |
| {ref}`reference-release-notes-16-06` | 2016-Jul | 2017-Dec | — | 14.04 LTS or 16.04 LTS |
| {ref}`reference-release-notes-16-03` | 2016-Apr | 2017-Apr | — | 14.04 LTS |
