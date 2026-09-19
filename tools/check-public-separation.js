#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const forbidden = String.fromCharCode(106,97,109,97,99,105,116,97).toLowerCase();
const skipDirs = new Set([".git", "node_modules"]);
const skipExt = new Set([".png",".jpg",".jpeg",".gif",".webp",".ico",".woff",".woff2",".ttf",".pdf",".zip"]);
const hits = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (skipDirs.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    const rel = path.relative(root, full).replace(/\\/g, "/");

    if (rel.toLowerCase().includes(forbidden)) hits.push(`path: ${rel}`);

    if (entry.isDirectory()) {
      walk(full);
      continue;
    }

    if (skipExt.has(path.extname(entry.name).toLowerCase())) continue;

    let content;
    try {
      content = fs.readFileSync(full, "utf8");
    } catch {
      continue;
    }
    if (content.toLowerCase().includes(forbidden)) hits.push(`content: ${rel}`);
  }
}

walk(root);

if (hits.length) {
  console.error("Public separation check failed.");
  hits.forEach((hit) => console.error(`- ${hit}`));
  process.exit(1);
}

console.log("Public separation check passed.");
