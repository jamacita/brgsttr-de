#!/usr/bin/env node

/**
 * BRGSTTR radar validation
 *
 * Checks the internal radar data source for:
 * - duplicate names
 * - missing required fields
 * - invalid taxonomy values
 * - wrong A-Z letter assignment
 * - non-alphabetical ordering inside the data source
 * - invalid optional governance fields
 *
 * Usage:
 *   node tools/validate-radar.js
 */

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const file = path.join(root, "_internal", "radar.json");

const data = JSON.parse(fs.readFileSync(file, "utf8"));
const errors = [];

const allowedKinds = new Set(Object.keys(data.taxonomy || {}));
const allowedStatuses = new Set(["active", "legacy", "watch", "review"]);
const allowedSensitivities = new Set(["low", "medium", "high"]);
const allowedSourceTypes = new Set(["observation-context", "feedback", "submission", "product-use", "concept"]);
const entries = Array.isArray(data.entries) ? data.entries : [];

if (!entries.length) {
  errors.push("No entries found in _internal/radar.json.");
}

const seen = new Map();

function expectedLetter(name) {
  return String(name || "").trim().charAt(0).toUpperCase();
}

function sortKey(entry) {
  return `${entry.letter || ""}\u0000${String(entry.name || "").toLocaleLowerCase("de-DE").replace("°", "")}`;
}

function validateOptionalEnum(entry, index, field, allowed) {
  if (entry[field] !== undefined && !allowed.has(entry[field])) {
    errors.push(`entry[${index}]: invalid ${field} "${entry[field]}".`);
  }
}

entries.forEach((entry, index) => {
  const ref = `entry[${index}]`;

  if (!entry.name || typeof entry.name !== "string") {
    errors.push(`${ref}: missing or invalid name.`);
  }

  if (!entry.letter || typeof entry.letter !== "string") {
    errors.push(`${ref}: missing or invalid letter.`);
  }

  if (!entry.kind || typeof entry.kind !== "string") {
    errors.push(`${ref}: missing or invalid kind.`);
  } else if (!allowedKinds.has(entry.kind)) {
    errors.push(`${ref}: invalid kind "${entry.kind}".`);
  }

  if (entry.visible !== true) {
    errors.push(`${ref}: visible must be true for the public radar list.`);
  }

  if (entry.name && entry.letter && expectedLetter(entry.name) !== entry.letter) {
    errors.push(`${ref}: letter "${entry.letter}" does not match name "${entry.name}".`);
  }

  validateOptionalEnum(entry, index, "status", allowedStatuses);
  validateOptionalEnum(entry, index, "sensitivity", allowedSensitivities);
  validateOptionalEnum(entry, index, "sourceType", allowedSourceTypes);

  if (entry.lastReviewed !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(entry.lastReviewed)) {
    errors.push(`${ref}: lastReviewed must use YYYY-MM-DD.`);
  }

  const normalizedName = String(entry.name || "").trim().toLocaleLowerCase("de-DE");
  if (seen.has(normalizedName)) {
    errors.push(`${ref}: duplicate name "${entry.name}" also appears at entry[${seen.get(normalizedName)}].`);
  } else {
    seen.set(normalizedName, index);
  }
});

const sorted = [...entries].sort((a, b) => sortKey(a).localeCompare(sortKey(b), "de-DE"));
entries.forEach((entry, index) => {
  if (entry.name !== sorted[index].name || entry.letter !== sorted[index].letter) {
    errors.push(`entries: list is not sorted at index ${index}; expected "${sorted[index].name}", found "${entry.name}".`);
  }
});

if (errors.length) {
  console.error("Radar validation failed:");
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log(`Radar validation passed: ${entries.length} entries checked.`);
