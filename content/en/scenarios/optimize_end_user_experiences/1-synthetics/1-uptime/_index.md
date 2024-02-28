---
title: 1. Uptime Test
weight: 1
---

## Introduction

The simplest way to keep an eye on endpoint availability is with an [Uptime test](https://docs.splunk.com/observability/en/synthetics/uptime-test/uptime-test.html). This lightweight test can run internally or externally around the world, as frequently as every minute. Because this is the easiest (and cheapest!) test to set up, and because this is ideal for monitoring availability of your most critical enpoints and ports, let's start here.

## Pre-requisites

- Publicly accessible HTTP(S) endpoint(s) to test
- Access to Splunk Observability Cloud
