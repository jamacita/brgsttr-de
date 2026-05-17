#!/usr/bin/env node

/**
 * BRGSTTR public radar hygiene check
 *
 * Runs in the public website repository and verifies that:
 * - no structured radar JSON source is committed to public website paths
 * - the rendered static radar page keeps noindex protection
 * - the rendered static radar page keeps interpretation boundaries
 * - the rendered static radar page keeps generator markers
 */

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const errors = [];

function exists(relativePath) {
  return fs.existsSync(path.join(root, relativePath));
}

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

if (exists("assets/radar.json")) {
  errors.push("assets/radar.json must not exist in the public website repository.");
}

if (exists("_internal/radar.json")) {
  errors.push("_internal/radar.json must not exist in the public website repository; keep the master source in the private repository.");
}

const htmlPath = "radar/index.html";
if (!exists(htmlPath)) {
  errors.push("radar/index.html is missing.");
} else {
  const html = read(htmlPath);
  const requiredSnippets = [
    "noindex, nofollow, noarchive, noimageindex, nosnippet",
    "not a client list",
    "not a representation of relationship, endorsement or use",
    "<!-- radar-list:start -->",
    "<!-- radar-list:end -->"
  ];

  for (const snippet of requiredSnippets) {
    if (!html.includes(snippet)) {
      errors.push(`radar/index.html is missing required snippet: ${snippet}`);
    }
  }
}

const robotsPath = "robots.txt";
if (!exists(robotsPath)) {
  errors.push("robots.txt is missing.");
} else {
  const robots = read(robotsPath);
  for (const line of ["Disallow: /radar/", "Disallow: /_internal/"]) {
    if (!robots.includes(line)) {
      errors.push(`robots.txt is missing ${line}`);
    }
  }
}

if (exists(".nojekyll")) {
  errors.push(".nojekyll must not exist unless _internal publication controls are redesigned.");
}

if (errors.length) {
  console.error("Public radar hygiene check failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("Public radar hygiene check passed.");
