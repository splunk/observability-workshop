#!/usr/bin/env node

import { chromium, firefox, webkit } from "playwright";

const appUrl = process.env.RUM_SIMULATOR_URL ?? "http://127.0.0.1:18080";
const users = Number.parseInt(process.env.RUM_SIMULATOR_USERS ?? "5", 10);
const rounds = Number.parseInt(process.env.RUM_SIMULATOR_ROUNDS ?? "6", 10);
const thinkTimeMs = Number.parseInt(process.env.RUM_SIMULATOR_THINK_TIME_MS ?? "7000", 10);
const staggerMs = Number.parseInt(process.env.RUM_SIMULATOR_STAGGER_MS ?? "1200", 10);
const settleMs = Number.parseInt(process.env.RUM_SIMULATOR_SETTLE_MS ?? "15000", 10);
const sessionTargetMs = Number.parseInt(process.env.RUM_SIMULATOR_SESSION_TARGET_MS ?? "28000", 10);
const cooldownMs = Number.parseInt(process.env.RUM_SIMULATOR_COOLDOWN_MS ?? "12000", 10);
const concurrency = Number.parseInt(process.env.RUM_SIMULATOR_CONCURRENCY ?? "1", 10);
const configuredBrowsers = (process.env.RUM_SIMULATOR_BROWSERS ?? "chromium,firefox,webkit")
  .split(",")
  .map((value) => value.trim().toLowerCase())
  .filter(Boolean);

const browserFactories = {
  chromium,
  firefox,
  webkit
};

const browserProfiles = {
  chromium: {
    locale: "en-US",
    viewport: { width: 1440, height: 900 }
  },
  firefox: {
    locale: "en-GB",
    viewport: { width: 1366, height: 768 }
  },
  webkit: {
    locale: "pt-BR",
    viewport: { width: 1512, height: 982 }
  }
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function chooseBrowserName(userNumber, roundNumber) {
  const index = (roundNumber + userNumber - 2) % configuredBrowsers.length;
  return configuredBrowsers[index] in browserFactories ? configuredBrowsers[index] : "chromium";
}

async function runUser(userNumber, roundNumber) {
  const startedAt = Date.now();
  const browserName = chooseBrowserName(userNumber, roundNumber);
  const browserType = browserFactories[browserName];
  const profile = browserProfiles[browserName];
  const browser = await browserType.launch({ headless: true });
  const context = await browser.newContext({
    viewport: profile.viewport,
    userAgent: `ibobs-rum-simulator/${browserName}/${roundNumber}-${userNumber}`,
    locale: profile.locale,
    colorScheme: userNumber % 2 === 0 ? "light" : "dark"
  });
  const page = await context.newPage();

  await page.goto(`${appUrl}/?persona=user-${roundNumber}-${userNumber}`, {
    waitUntil: "domcontentloaded"
  });
  await page.waitForLoadState("networkidle");

  await page.evaluate(
    ([user, round, activeBrowser]) => {
      window.localStorage.setItem("ibobs-sim-user", `user-${round}-${user}`);
      window.sessionStorage.setItem("ibobs-sim-session", crypto.randomUUID());
      window.localStorage.setItem("ibobs-sim-browser", activeBrowser);
    },
    [userNumber, roundNumber, browserName]
  );

  await page.getByRole("button", { name: "Submit Claim Status" }).click();
  await page.waitForTimeout(thinkTimeMs);

  await page.getByRole("button", { name: "Check Coverage" }).click();
  await page.waitForTimeout(thinkTimeMs);

  await page.getByRole("button", { name: "Search FAQ" }).click();
  await page.waitForTimeout(3000);

  const elapsedMs = Date.now() - startedAt;
  const remainingMs = Math.max(0, sessionTargetMs - elapsedMs);
  await page.waitForTimeout(Math.max(settleMs, remainingMs));

  await context.close();
  await browser.close();

  return browserName;
}

async function main() {
  for (let round = 1; round <= rounds; round += 1) {
    console.log(
      JSON.stringify({ round, users, appUrl, browsers: configuredBrowsers, concurrency, cooldownMs })
    );

    for (let start = 1; start <= users; start += concurrency) {
      const tasks = [];

      for (let user = start; user < Math.min(start + concurrency, users + 1); user += 1) {
        tasks.push(
          (async () => {
            await sleep((user - start) * staggerMs);
            const browserName = await runUser(user, round);
            console.log(JSON.stringify({ round, user, browser: browserName, status: "completed" }));
          })()
        );
      }

      await Promise.all(tasks);
      await sleep(cooldownMs);
    }
  }
}

await main();
