# radar. maintenance note

## 1. Purpose

`/radar/` is a quiet A-Z orientation layer for entities, organisations, brands, formats and public bodies that have appeared in interaction, observation, feedback, concept, product or value-contribution contexts connected with Jamacita or BRGSTTR.

It is not a client list, partnership statement, endorsement claim, public attribution archive or statement of consent by any listed entity.

## 2. Source of record

The structured maintenance source is private and must not be committed to the public website repository.

```text
Private repository: jamacita/jamacita-method-private
Private path: brgsttr/radar/radar.json
```

The public website repository contains only the rendered static HTML page:

```text
/radar/index.html
```

The public HTML list should be regenerated from the private JSON source when the private source changes.

## 3. Visible display policy

The public page should remain:

1. Alphabetical.
2. Sector-neutral.
3. Without visible categories.
4. Without rankings.
5. Without explanatory claims per entry.
6. Without logos or external links per entry.

## 4. Internal taxonomy

The private `kind` field uses exactly these values:

1. `entity`
2. `format`
3. `platform-app`
4. `public-body`
5. `place-location`
6. `infrastructure-service-system`

Optional `context` values may be used for maintenance clarity where the primary category alone is not sufficient.

## 5. Validation and build

Use the private source explicitly:

```bash
RADAR_SOURCE=/absolute/path/to/private/radar.json node tools/validate-radar.js
RADAR_SOURCE=/absolute/path/to/private/radar.json node tools/build-radar.js
```

The public repository workflow checks publication hygiene only. It verifies that no radar JSON source exists in the public website repository and that the rendered HTML keeps the required protection and interpretation markers.

## 6. Revision principle

The page is selectively maintained, non-exhaustive and subject to quiet revision.
