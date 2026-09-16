"""Storage for Virasat.

Plain sqlite3, no ORM, so anyone who reads Python can follow it.
The database is a single file (virasat.db) created on first run.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "virasat.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY, slug TEXT UNIQUE, name TEXT, state TEXT, region TEXT,
    tagline TEXT, intro TEXT, hero TEXT, accent TEXT, best_time TEXT,
    languages TEXT, tags TEXT
);
CREATE TABLE IF NOT EXISTS place_images (
    id INTEGER PRIMARY KEY, place_id INTEGER, url TEXT, caption TEXT, ord INTEGER
);
CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY, place_id INTEGER, title TEXT, era TEXT, language TEXT,
    source TEXT, passage TEXT, note TEXT
);
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY, handle TEXT UNIQUE, name TEXT, place_id INTEGER,
    bio TEXT, craft TEXT, avatar TEXT, monetized INTEGER DEFAULT 0,
    payout TEXT, joined TEXT
);
CREATE TABLE IF NOT EXISTS interests (
    member_id INTEGER, place_id INTEGER, PRIMARY KEY (member_id, place_id)
);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY, member_id INTEGER, place_id INTEGER, kind TEXT,
    title TEXT, body TEXT, cover TEXT, created TEXT
);
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY, post_id INTEGER, url TEXT, caption TEXT, ord INTEGER
);
CREATE TABLE IF NOT EXISTS appreciations (
    post_id INTEGER, member_id INTEGER, PRIMARY KEY (post_id, member_id)
);
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY, post_id INTEGER, member_id INTEGER, body TEXT, created TEXT
);
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY, member_id INTEGER, place_id INTEGER, title TEXT,
    summary TEXT, details TEXT, price INTEGER, duration TEXT, capacity INTEGER,
    image TEXT, created TEXT
);
CREATE TABLE IF NOT EXISTS artworks (
    id INTEGER PRIMARY KEY, member_id INTEGER, place_id INTEGER, title TEXT,
    medium TEXT, story TEXT, price INTEGER, image TEXT, sold INTEGER DEFAULT 0,
    created TEXT
);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY, kind TEXT, ref_id INTEGER, from_id INTEGER, to_id INTEGER,
    message TEXT, date TEXT, guests INTEGER, amount INTEGER, status TEXT, created TEXT
);
"""


def connect():
    """Open the database. Rows come back like dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query(sql, args=(), one=False):
    with connect() as conn:
        rows = conn.execute(sql, args).fetchall()
    return (rows[0] if rows else None) if one else rows


def execute(sql, args=()):
    """Run a write and return the new row id."""
    with connect() as conn:
        cur = conn.execute(sql, args)
        conn.commit()
        return cur.lastrowid


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def init(reset=False):
    """Create the tables, and fill them with the starter content once."""
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    with connect() as conn:
        conn.executescript(SCHEMA)
        conn.commit()
    if not query("SELECT id FROM places LIMIT 1"):
        import seed_data
        seed_data.fill()
