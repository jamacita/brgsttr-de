#!/usr/bin/env node

/**
 * BRGSTTR radar builder
 *
 * Builds the visible A-Z radar HTML block from a private radar source file.
 * The public website repository must not contain the radar JSON source.
 *
 * Usage:
 *   RADAR_SOURCE=/path/to/private/radar.json node tools/build-radar.js
 *   RADAR_SOURCE=/path/to/private/radar.json node tools/build-radar.js --check
 */

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const htmlFile = path.join(root, "radar", "index.html");
const checkOnly = process.argv.includes("--check");

const candidateSources = [
  process.env.RADAR_SOURCE,
  path.resolve(root, "..", "jamacita-method-private", "brgsttr", "radar", "radar.json"),
  path.resolve(root, "..", "brgsttr-radar-private", "radar.json")
].filter(Boolean);

const sourceFile = candidateSources.find((candidate) => fs.existsSync(candidate));

if (!sourceFile) {
  console.error("Radar build failed: private radar source not found.");
  console.error("Set RADAR_SOURCE=/absolute/path/to/private/radar.json.");
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(sourceFile, "utf8"));
const html = fs.readFileSync(htmlFile, "utf8");
const entries = data.entries.filter((entry) => entry.visible === true);

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;");
}

function sortKey(entry) {
  return `${entry.letter}\u0000${entry.name.toLocaleLowerCase("de-DE").replace("°", "")}`;
}

function buildList() {
  const grouped = new Map();
  [...entries]
    .sort((a, b) => sortKey(a).localeCompare(sortKey(b), "de-DE"))
    .forEach((entry) => {
      if (!grouped.has(entry.letter)) grouped.set(entry.letter, []);
      grouped.get(entry.letter).push(entry);
    });

  const articles = [];
  for (const [letter, items] of grouped.entries()) {
    const lines = [];
    lines.push("        <article class=\"panel\">");
    lines.push(`          <h2>${escapeHtml(letter)}</h2>`);
    lines.push("          <ul class=\"plain-list\">");
    for (const entry of items) {
      const context = entry.context ? ` data-context=\"${escapeHtml(entry.context)}\"` : "";
      lines.push(`            <li data-kind=\"${escapeHtml(entry.kind)}\"${context}>${escapeHtml(entry.name)}</li>`);
    }
    lines.push("          </ul>");
    lines.push("        </article>");
    articles.push(lines.join("\n"));
  }
  return articles.join("\n");
}

const start = "        <!-- radar-list:start -->";
const end = "        <!-- radar-list:end -->";

if (!html.includes(start) || !html.includes(end)) {
  console.error("Radar build failed: missing radar-list markers in radar/index.html.");
  process.exit(1);
}

const block = buildList();
const pattern = new RegExp(`${start}[\\s\\S]*?${end}`);
const replacement = `${start}\n${block}\n        ${end.trim()}`;
const nextHtml = html.replace(pattern, replacement);

if (checkOnly) {
  if (nextHtml !== html) {
    console.error("Radar build check failed: radar/index.html is not synchronized with the private radar source.");
    process.exit(1);
  }
  console.log("Radar build check passed: radar/index.html is synchronized.");
  process.exit(0);
}

fs.writeFileSync(htmlFile, nextHtml, "utf8");
console.log(`Radar HTML block rebuilt from ${sourceFile}.`);
