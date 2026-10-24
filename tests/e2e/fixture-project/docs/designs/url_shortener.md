# URL Shortener Service

## Objective

Give users short links (for example `https://sho.rt/aB3x9`) that redirect to
long URLs, so links fit in SMS messages and printed material.

## Background

Marketing currently pastes full campaign URLs with UTM parameters into SMS
campaigns. Long links are truncated by some carriers and cost extra segments.

## Requirements

1. Create a short code for any valid `http` or `https` URL.
2. Redirect `GET /<code>` to the long URL with HTTP 301.
3. Show click counts per code to the link owner.
4. Codes never expire.

## Design

### Code generation

Each new link takes the next value of a global counter and encodes it in
base62. The counter lives in a single Postgres sequence.

### Storage

One table, `links(code TEXT PRIMARY KEY, long_url TEXT, owner_id BIGINT,
clicks BIGINT, created_at TIMESTAMPTZ)`.

### Redirect path

The redirect handler reads the row, increments `clicks` in the same
transaction, then returns 301.

### Analytics

The dashboard reads `clicks` straight from the `links` table.

## Alternatives considered

Random 7-character codes were rejected because collisions need a retry loop.

## Open questions

- Do we need custom vanity codes?
