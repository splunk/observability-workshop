---
title: 1. Real Browser Test
weight: 1
---

## Introduction

This part of the workshop walks you through using the [**Chrome DevTools Recorder**](https://developer.chrome.com/docs/devtools/recorder/) to create a synthetic transaction against a Splunk demonstration instance. You'll export that recording as JSON and use it to create a **Splunk Synthetic Monitoring Real Browser Test** that runs from the cloud, on a schedule, from multiple global locations.

### What is a Real Browser Test?

A Real Browser Test (RBT) is a synthetic check where Splunk Synthetic Monitoring spins up a **full Chromium browser** in one of its global cloud locations, loads your site, and drives it through a sequence of user actions — clicks, form input, navigation — exactly as a real person would. Because it's a real browser, it executes JavaScript, runs your full third-party dependency graph, applies CSS, and captures everything a regular user's browser does. That makes RBTs ideal for monitoring user journeys end to end: login, checkout, search, dashboard load.

The trade-off versus a simple HTTP uptime check is cost and run frequency — a real-browser run takes 10–30 seconds and consumes more capacity, so RBTs are typically scheduled every 1–5 minutes per location, where uptime checks can run every minute against many endpoints at little cost.

### Why start with the Chrome DevTools Recorder?

You can hand-author a Synthetic test step by step in the Splunk UI, but recording the journey first is faster and less error-prone — the recorder captures multiple resilient selectors for every element you click (CSS, XPath, etc.) so the resulting test is less likely to break the first time a developer tweaks a class name. The exported JSON is also a portable artefact you can check into version control, share with teammates, or feed into other tooling that speaks the same recording format.
