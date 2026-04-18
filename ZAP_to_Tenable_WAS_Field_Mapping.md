# ZAP to Tenable WAS Mapping

## Core Scan Data Mapping

| ZAP sourcetype | Dashboards | Best Tenable WAS equivalent | Fit |
|---|---|---|---|
| `zap:alert` | Overview, Alerts | Findings table | Good |
| `zap:alert:evidence` | Alerts Detail | Finding detail / evidence fields, not in listed table | Partial |
| `zap:scan` | Scan Activity | Scan activity / scan history | Partial |
| `zap:site` | Affected URLs | Application / asset context | Partial |
| `zap:spider` | Spider | Crawl / discovery / spider activity | Weak |

## `zap:alert` → Tenable WAS Findings

| ZAP concept | Tenable WAS column |
|---|---|
| alert name | `Name` |
| alert or rule id | `Plugin ID` |
| rule family or category | `Family` |
| severity or risk | `Severity` |
| first detected | `First Seen` |
| last detected | `Last Updated` |
| current status | `State` |
| affected asset or application | `Application Name`, `Application ID`, `ID` |
| asset IP | `IPv4 Address` |
| prioritization | `VPR` |
| base severity score | `CVSSv2 Base Score` |
| asset tagging | `Tags` |

## `zap:alert:evidence` → Not covered by listed findings table columns

The listed Tenable WAS findings columns do **not** include:

- URL
- path
- parameter
- evidence text
- request or response data

So `zap:alert:evidence` does **not** map directly from the listed columns.

## `zap:scan` → Partial only

Closest listed fields:

- `First Seen`
- `Last Seen`
- `Last Updated`

These are finding or asset timestamps, **not full scan lifecycle fields**.

So `zap:scan` does **not** map cleanly from the listed findings columns.

## `zap:site` → Partial application or asset mapping

Closest listed fields:

- `Application Name`
- `Application ID`
- `ID`
- `IPv4 Address`
- `Tags`

This supports application inventory style views, but the listed Tenable fields do **not** include:

- URL
- hostname
- FQDN
- path
- page or site tree

So `Affected URLs` is better replaced with **Affected Applications**.

## `zap:spider` → Weak mapping

ZAP spider data is crawl and discovery telemetry such as:

- crawled URLs
- discovered pages
- spider status
- crawl counts

The listed Tenable WAS findings columns do not expose that kind of dataset.

So `zap:spider` has **no real direct mapping** from the listed columns.

## Practical Dashboard Mapping

| Current dashboard | ZAP source | Tenable WAS replacement |
|---|---|---|
| Overview | `zap:alert` | Findings Overview |
| Alerts | `zap:alert` | Findings |
| Alerts Detail | `zap:alert:evidence` | Finding Detail, but not from listed table alone |
| Scan Activity | `zap:scan` | Needs scan metadata source |
| Affected URLs | `zap:site` | Affected Applications |
| Spider | `zap:spider` | No equivalent from listed fields |

## Bottom Line

### Clean mapping
- `zap:alert` → **Tenable WAS Findings**

### Partial mapping
- `zap:scan` → scan metadata, not findings table
- `zap:site` → application or asset context, not URLs

### No usable mapping from listed findings columns
- `zap:alert:evidence`
- `zap:spider`

## Better Tenable WAS dashboard naming

Instead of:

- Alerts
- Alerts Detail
- Scan Activity
- Affected URLs
- Spider

Use:

- **Findings Overview**
- **Findings**
- **Finding Detail**
- **Affected Applications**
- **Scan History**
- **Crawl Activity** only if you have a separate WAS crawl dataset
