"""Redirect handler for the URL shortener (see docs/designs/url_shortener.md)."""

import psycopg


def redirect(conn: psycopg.Connection, code: str) -> tuple[int, dict[str, str]]:
  with conn.transaction():
    row = conn.execute(
        "SELECT long_url FROM links WHERE code = %s FOR UPDATE", (code,)
    ).fetchone()
    if row is None:
      return 404, {}
    conn.execute("UPDATE links SET clicks = clicks + 1 WHERE code = %s", (code,))
  return 301, {"Location": row[0]}
