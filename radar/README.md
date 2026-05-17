# radar. maintenance note

## 1. Purpose

`/radar/` is a quiet A-Z orientation layer for entities, organisations, brands, formats and public bodies that have appeared in interaction, observation, feedback, concept, product or value-contribution contexts connected with Jamacita or BRGSTTR.

It is not a client list, partnership statement, endorsement claim, public attribution archive or statement of consent by any listed entity.

## 2. Source of record

The structured maintenance source is:

```text
/assets/radar.json
```

The public HTML page remains static and deliberately simple:

```text
/radar/index.html
```

The HTML list should be kept synchronized with the JSON source.

## 3. Visible display policy

The public page should remain:

1. Alphabetical.
2. Sector-neutral.
3. Without visible categories.
4. Without rankings.
5. Without explanatory claims per entry.
6. Without logos or external links per entry.

## 4. Internal taxonomy

The internal `kind` field uses exactly these values:

1. `entity`
2. `format`
3. `platform-app`
4. `public-body`
5. `place-location`
6. `infrastructure-service-system`

Optional `context` values may be used for maintenance clarity where the primary category alone is not sufficient.

## 5. Validation

Run:

```bash
node tools/validate-radar.js
```

The validation checks:

1. Duplicate names.
2. Missing fields.
3. Invalid taxonomy values.
4. Letter assignment.
5. Alphabetical ordering.

## 6. Revision principle

The page is selectively maintained, non-exhaustive and subject to quiet revision.
