// @ts-check
const { defineConfig, devices } = require('@playwright/test');

// Without BASE_URL the suite runs against a local production build served under the Pages subpath.
const LOCAL_URL = 'http://127.0.0.1:4173/catharsis-as-a-service/';
const baseURL = process.env.BASE_URL || LOCAL_URL;

module.exports = defineConfig({
  testDir: 'tests',
  timeout: 90_000,
  expect: { timeout: 15_000 },
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['list'], ['github']] : [['list']],
  outputDir: 'test-results',
  use: {
    baseURL,
    locale: 'en-US',
    reducedMotion: 'reduce',
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: process.env.BASE_URL
    ? undefined
    : {
        command: 'scripts/preview.sh',
        url: LOCAL_URL,
        timeout: 300_000,
        reuseExistingServer: !process.env.CI,
      },
});
