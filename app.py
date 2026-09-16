"""Virasat — a club for people who are in love with a place.

Everyone here is the same kind of member: you can write, post photographs, paintings,
old texts and stories. If you also want to sell an experience or a piece of art, you
turn on selling in your profile and a dashboard appears inside the same site.

Flask and HTML templates. There is no JavaScript anywhere in this project.
Run it with:  python app.py
"""

from pathlib import Path
from uuid import uuid4

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from markupsafe import Markup, escape
from werkzeug.utils import secure_filename

import db

BASE = Path(__file__).parent
UPLOAD_DIR = BASE / "static" / "uploads"
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# What a seller keeps, and what goes to the place's preservation fund.
FUND_SHARE = 0.10

POST_KINDS = [
    ("story", "Story"),
    ("photo", "Photographs"),
    ("painting", "Painting or craft"),
    ("writing", "Writing"),
    ("text", "Old text"),
]

app = Flask(__name__)
app.secret_key = "virasat-prototype-key"          # fine for a prototype on your own machine
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


# --------------------------------------------------------------------------- helpers

def current_member():
    """The signed-in member row, or None."""
    mid = session.get("member_id")
    if not mid:
        return None
    return db.query("SELECT * FROM members WHERE id = ?", (mid,), one=True)


def chosen_place_ids():
    """Places this visitor said they love."""
    me = current_member()
    if me:
        rows = db.query("SELECT place_id FROM interests WHERE member_id = ?", (me["id"],))
        if rows:
            return [r["place_id"] for r in rows]
    return session.get("interests", [])


def similar_places(place_ids, limit=3):
    """Other places that share the most tags with the ones already chosen."""
    if not place_ids:
        return []
    chosen = db.query(f"SELECT * FROM places WHERE id IN ({','.join('?' * len(place_ids))})",
                      tuple(place_ids))
    liked_tags = set()
    for p in chosen:
        liked_tags.update(p["tags"].split(","))
    others = db.query(f"SELECT * FROM places WHERE id NOT IN ({','.join('?' * len(place_ids))})",
                      tuple(place_ids))
    scored = []
    for p in others:
        shared = liked_tags & set(p["tags"].split(","))
        if shared:
            scored.append((len(shared), sorted(shared), p))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [{"place": p, "shared": tags} for _, tags, p in scored[:limit]]


def save_upload(file_storage):
    """Store one uploaded image under static/uploads and return its URL."""
    if not file_storage or not file_storage.filename:
        return ""
    name = secure_filename(file_storage.filename)
    suffix = Path(name).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        return ""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored = f"{uuid4().hex[:12]}{suffix}"
    file_storage.save(UPLOAD_DIR / stored)
    return url_for("static", filename=f"uploads/{stored}")


def rupees(amount):
    """Format a number the Indian way: 1,80,000."""
    amount = int(round(amount or 0))
    text = str(abs(amount))
    if len(text) > 3:
        head, tail = text[:-3], text[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        text = ",".join(parts + [tail])
    return f"₹{'-' if amount < 0 else ''}{text}"


def words(text):
    """Wrap every word in a span so CSS can lift them in one after another.

    This is how the headings animate without a line of JavaScript: Python does the
    splitting, the stylesheet does the moving.
    """
    spans = [f'<span class="w" style="--i:{i}"><span>{escape(word)}</span></span>'
             for i, word in enumerate((text or "").split())]
    return Markup(" ".join(spans))


app.jinja_env.filters["rupees"] = rupees
app.jinja_env.filters["words"] = words
app.jinja_env.filters["paragraphs"] = lambda body: [p for p in (body or "").split("\n\n") if p.strip()]


@app.context_processor
def inject_globals():
    return dict(me=current_member(), all_places=db.query("SELECT * FROM places ORDER BY name"),
                post_kinds=POST_KINDS, fund_share=FUND_SHARE,
                theme=session.get("theme", "dark"), here=request.path)


@app.post("/theme")
def switch_theme():
    """Dark by default; the choice is remembered in the session, no JavaScript involved."""
    session["theme"] = "light" if session.get("theme", "dark") == "dark" else "dark"
    return redirect(request.form.get("next") or url_for("home"))


def member_by_id(mid):
    return db.query("SELECT * FROM members WHERE id = ?", (mid,), one=True)


def post_with_extras(row):
    """Attach author, place, images and counts to a post row."""
    post = dict(row)
    post["author"] = member_by_id(row["member_id"])
    post["place"] = db.query("SELECT * FROM places WHERE id = ?", (row["place_id"],), one=True)
    post["images"] = db.query("SELECT * FROM images WHERE post_id = ? ORDER BY ord", (row["id"],))
    post["likes"] = len(db.query("SELECT * FROM appreciations WHERE post_id = ?", (row["id"],)))
    post["comment_count"] = len(db.query("SELECT id FROM comments WHERE post_id = ?", (row["id"],)))
    return post


def feed_posts(place_ids=None, limit=30):
    if place_ids:
        marks = ",".join("?" * len(place_ids))
        rows = db.query(f"SELECT * FROM posts WHERE place_id IN ({marks})"
                        f" ORDER BY created DESC LIMIT ?", (*place_ids, limit))
    else:
        rows = db.query("SELECT * FROM posts ORDER BY created DESC LIMIT ?", (limit,))
    return [post_with_extras(r) for r in rows]


def listing_rows(table, place_ids=None, member_id=None, limit=50):
    where, args = [], []
    if place_ids:
        where.append(f"place_id IN ({','.join('?' * len(place_ids))})")
        args += list(place_ids)
    if member_id:
        where.append("member_id = ?")
        args.append(member_id)
    clause = f"WHERE {' AND '.join(where)}" if where else ""
    rows = db.query(f"SELECT * FROM {table} {clause} ORDER BY created DESC LIMIT ?", (*args, limit))
    out = []
    for r in rows:
        item = dict(r)
        item["author"] = member_by_id(r["member_id"])
        item["place"] = db.query("SELECT * FROM places WHERE id = ?", (r["place_id"],), one=True)
        out.append(item)
    return out


# --------------------------------------------------------------------------- pages

@app.route("/")
def home():
    place_ids = chosen_place_ids()
    if not place_ids:
        counts = dict(
            members=len(db.query("SELECT id FROM members")),
            posts=len(db.query("SELECT id FROM posts")),
            places=len(db.query("SELECT id FROM places")),
            texts=len(db.query("SELECT id FROM texts")),
        )
        return render_template("landing.html", counts=counts,
                               recent=feed_posts(limit=6))
    places = db.query(f"SELECT * FROM places WHERE id IN ({','.join('?' * len(place_ids))})",
                      tuple(place_ids))
    return render_template(
        "feed.html",
        places=places,
        similar=similar_places(place_ids),
        posts=feed_posts(place_ids),
        texts=db.query(f"SELECT * FROM texts WHERE place_id IN ({','.join('?' * len(place_ids))})"
                       f" ORDER BY RANDOM() LIMIT 3", tuple(place_ids)),
        experiences=listing_rows("experiences", place_ids, limit=6),
        artworks=listing_rows("artworks", place_ids, limit=6),
    )


@app.post("/interests")
def set_interests():
    picked = [int(v) for v in request.form.getlist("place")][:4]
    if len(picked) < 1:
        flash("Choose at least one place you love.")
        return redirect(url_for("home"))
    session["interests"] = picked
    me = current_member()
    if me:
        db.execute("DELETE FROM interests WHERE member_id = ?", (me["id"],))
        for pid in picked:
            db.execute("INSERT OR IGNORE INTO interests (member_id, place_id) VALUES (?,?)",
                       (me["id"], pid))
    return redirect(url_for("home"))


@app.get("/rechoose")
def rechoose():
    session.pop("interests", None)
    me = current_member()
    if me:
        db.execute("DELETE FROM interests WHERE member_id = ?", (me["id"],))
    return redirect(url_for("home"))


@app.get("/places")
def places_index():
    return render_template("places.html", places=db.query("SELECT * FROM places ORDER BY name"))


@app.get("/place/<slug>")
def place(slug):
    p = db.query("SELECT * FROM places WHERE slug = ?", (slug,), one=True)
    if not p:
        abort(404)
    return render_template(
        "place.html", place=p,
        gallery=db.query("SELECT * FROM place_images WHERE place_id = ? ORDER BY ord", (p["id"],)),
        texts=db.query("SELECT * FROM texts WHERE place_id = ?", (p["id"],)),
        posts=feed_posts([p["id"]]),
        experiences=listing_rows("experiences", [p["id"]]),
        artworks=listing_rows("artworks", [p["id"]]),
        members=db.query("SELECT * FROM members WHERE place_id = ? ORDER BY name", (p["id"],)),
        similar=similar_places([p["id"]]),
    )


@app.get("/library")
def library():
    rows = db.query("SELECT * FROM texts ORDER BY place_id")
    texts = []
    for t in rows:
        item = dict(t)
        item["place"] = db.query("SELECT * FROM places WHERE id = ?", (t["place_id"],), one=True)
        texts.append(item)
    return render_template("library.html", texts=texts)


@app.get("/stories")
def stories_index():
    kind = request.args.get("kind", "")
    rows = (db.query("SELECT * FROM posts WHERE kind = ? ORDER BY created DESC", (kind,))
            if kind else db.query("SELECT * FROM posts ORDER BY created DESC"))
    return render_template("stories.html", posts=[post_with_extras(r) for r in rows], kind=kind)


@app.get("/post/<int:pid>")
def post(pid):
    row = db.query("SELECT * FROM posts WHERE id = ?", (pid,), one=True)
    if not row:
        abort(404)
    item = post_with_extras(row)
    comments = []
    for c in db.query("SELECT * FROM comments WHERE post_id = ? ORDER BY created", (pid,)):
        entry = dict(c)
        entry["author"] = member_by_id(c["member_id"])
        comments.append(entry)
    more = db.query("SELECT * FROM posts WHERE place_id = ? AND id != ? ORDER BY created DESC"
                    " LIMIT 3", (row["place_id"], pid))
    return render_template("post.html", post=item, comments=comments,
                           more=[post_with_extras(r) for r in more])


@app.post("/post/<int:pid>/comment")
def add_comment(pid):
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("post", pid=pid)))
    body = request.form.get("body", "").strip()
    if body:
        db.execute("INSERT INTO comments (post_id, member_id, body, created) VALUES (?,?,?,?)",
                   (pid, me["id"], body, db.now()))
    return redirect(url_for("post", pid=pid) + "#comments")


@app.post("/post/<int:pid>/appreciate")
def appreciate(pid):
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("post", pid=pid)))
    existing = db.query("SELECT * FROM appreciations WHERE post_id = ? AND member_id = ?",
                        (pid, me["id"]), one=True)
    if existing:
        db.execute("DELETE FROM appreciations WHERE post_id = ? AND member_id = ?", (pid, me["id"]))
    else:
        db.execute("INSERT INTO appreciations (post_id, member_id) VALUES (?,?)", (pid, me["id"]))
    return redirect(request.form.get("back") or url_for("post", pid=pid))


@app.route("/share", methods=["GET", "POST"])
def share():
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("share")))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        kind = request.form.get("kind", "story")
        place_id = int(request.form.get("place_id") or me["place_id"])
        if not title or not body:
            flash("A title and a few words are needed.")
            return render_template("share.html", form=request.form)
        uploads = [save_upload(f) for f in request.files.getlist("images")]
        uploads = [u for u in uploads if u]
        captions = request.form.getlist("captions")
        cover = uploads[0] if uploads else request.form.get("cover_url", "").strip()
        pid = db.execute(
            "INSERT INTO posts (member_id, place_id, kind, title, body, cover, created)"
            " VALUES (?,?,?,?,?,?,?)",
            (me["id"], place_id, kind, title, body, cover, db.now()))
        for i, url in enumerate(uploads[1:], start=0):
            caption = captions[i + 1] if len(captions) > i + 1 else ""
            db.execute("INSERT INTO images (post_id, url, caption, ord) VALUES (?,?,?,?)",
                       (pid, url, caption, i))
        flash("Posted. Thank you for adding to the record.")
        return redirect(url_for("post", pid=pid))
    return render_template("share.html", form={})


# --------------------------------------------------------------------------- experiences & art

@app.get("/experiences")
def experiences_index():
    return render_template("experiences.html", experiences=listing_rows("experiences"))


@app.get("/experience/<int:eid>")
def experience(eid):
    row = db.query("SELECT * FROM experiences WHERE id = ?", (eid,), one=True)
    if not row:
        abort(404)
    item = dict(row)
    item["author"] = member_by_id(row["member_id"])
    item["place"] = db.query("SELECT * FROM places WHERE id = ?", (row["place_id"],), one=True)
    return render_template("experience.html", exp=item)


@app.post("/experience/<int:eid>/request")
def request_experience(eid):
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("experience", eid=eid)))
    row = db.query("SELECT * FROM experiences WHERE id = ?", (eid,), one=True)
    guests = max(1, min(int(request.form.get("guests", 1)), row["capacity"]))
    db.execute(
        "INSERT INTO requests (kind, ref_id, from_id, to_id, message, date, guests, amount,"
        " status, created) VALUES (?,?,?,?,?,?,?,?,?,?)",
        ("experience", eid, me["id"], row["member_id"], request.form.get("message", "").strip(),
         request.form.get("date", db.today()), guests, row["price"] * guests, "pending", db.now()))
    flash(f"Asked {member_by_id(row['member_id'])['name']}. You will see the reply under Requests.")
    return redirect(url_for("my_requests"))


@app.get("/art")
def art_index():
    return render_template("art.html", artworks=listing_rows("artworks"))


@app.get("/artwork/<int:aid>")
def artwork(aid):
    row = db.query("SELECT * FROM artworks WHERE id = ?", (aid,), one=True)
    if not row:
        abort(404)
    item = dict(row)
    item["author"] = member_by_id(row["member_id"])
    item["place"] = db.query("SELECT * FROM places WHERE id = ?", (row["place_id"],), one=True)
    return render_template("artwork.html", art=item)


@app.post("/artwork/<int:aid>/request")
def request_artwork(aid):
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("artwork", aid=aid)))
    row = db.query("SELECT * FROM artworks WHERE id = ?", (aid,), one=True)
    offer = request.form.get("amount", "").strip()
    amount = int(offer) if offer.isdigit() else row["price"]
    db.execute(
        "INSERT INTO requests (kind, ref_id, from_id, to_id, message, date, guests, amount,"
        " status, created) VALUES (?,?,?,?,?,?,?,?,?,?)",
        ("art", aid, me["id"], row["member_id"], request.form.get("message", "").strip(),
         db.today(), 1, amount, "pending", db.now()))
    flash("Sent to the artist. You will see the reply under Requests.")
    return redirect(url_for("my_requests"))


@app.get("/requests")
def my_requests():
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("my_requests")))
    rows = db.query("SELECT * FROM requests WHERE from_id = ? ORDER BY created DESC", (me["id"],))
    return render_template("requests.html", requests=[decorate_request(r) for r in rows])


def decorate_request(row):
    item = dict(row)
    if row["kind"] == "experience":
        item["subject"] = db.query("SELECT * FROM experiences WHERE id = ?", (row["ref_id"],), one=True)
        item["link"] = url_for("experience", eid=row["ref_id"])
    else:
        item["subject"] = db.query("SELECT * FROM artworks WHERE id = ?", (row["ref_id"],), one=True)
        item["link"] = url_for("artwork", aid=row["ref_id"])
    item["from_member"] = member_by_id(row["from_id"])
    item["to_member"] = member_by_id(row["to_id"])
    return item


# --------------------------------------------------------------------------- members & selling

@app.get("/members")
def members_index():
    rows = db.query("SELECT * FROM members ORDER BY name")
    members = []
    for m in rows:
        item = dict(m)
        item["place"] = db.query("SELECT * FROM places WHERE id = ?", (m["place_id"],), one=True)
        item["posts"] = len(db.query("SELECT id FROM posts WHERE member_id = ?", (m["id"],)))
        members.append(item)
    return render_template("members.html", members=members)


@app.get("/member/<handle>")
def member(handle):
    m = db.query("SELECT * FROM members WHERE handle = ?", (handle,), one=True)
    if not m:
        abort(404)
    return render_template(
        "member.html", member=m,
        place=db.query("SELECT * FROM places WHERE id = ?", (m["place_id"],), one=True),
        posts=[post_with_extras(r) for r in
               db.query("SELECT * FROM posts WHERE member_id = ? ORDER BY created DESC", (m["id"],))],
        experiences=listing_rows("experiences", member_id=m["id"]),
        artworks=listing_rows("artworks", member_id=m["id"]),
    )


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        handle = request.form.get("handle", "").strip().lower()
        if handle:                                    # continue as an existing member
            m = db.query("SELECT * FROM members WHERE handle = ?", (handle,), one=True)
            if m:
                session["member_id"] = m["id"]
                session.pop("interests", None)
                return redirect(request.form.get("next") or url_for("home"))
        name = request.form.get("name", "").strip()
        if name:                                      # or make a new member
            new_handle = "".join(ch for ch in name.lower().replace(" ", "") if ch.isalnum())[:18]
            while db.query("SELECT id FROM members WHERE handle = ?", (new_handle,), one=True):
                new_handle += "1"
            place_id = int(request.form.get("place_id") or 1)
            mid = db.execute(
                "INSERT INTO members (handle, name, place_id, bio, craft, avatar, monetized,"
                " payout, joined) VALUES (?,?,?,?,?,?,?,?,?)",
                (new_handle, name, place_id, request.form.get("bio", "").strip(),
                 request.form.get("craft", "").strip(), "", 0, "", db.now()))
            session["member_id"] = mid
            flash(f"Welcome, {name}. Post whenever you like; selling is optional.")
            return redirect(request.form.get("next") or url_for("home"))
        flash("Pick a member to continue as, or tell us your name.")
    return render_template("signin.html", next=request.args.get("next", ""),
                           members=db.query("SELECT * FROM members ORDER BY name"))


@app.post("/signout")
def signout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/monetize", methods=["GET", "POST"])
def monetize():
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("monetize")))
    if request.method == "POST":
        db.execute("UPDATE members SET monetized = 1, payout = ? WHERE id = ?",
                   (request.form.get("payout", "UPI"), me["id"]))
        flash("Selling is on. Your dashboard is in the top bar.")
        return redirect(url_for("studio"))
    return render_template("monetize.html")


@app.post("/monetize/off")
def monetize_off():
    me = current_member()
    if me:
        db.execute("UPDATE members SET monetized = 0 WHERE id = ?", (me["id"],))
        flash("Selling is off. Your posts stay exactly where they are.")
    return redirect(url_for("member", handle=me["handle"]) if me else url_for("home"))


# --------------------------------------------------------------------------- seller dashboard

@app.get("/studio")
def studio():
    me = current_member()
    if not me:
        return redirect(url_for("signin", next=url_for("studio")))
    if not me["monetized"]:
        return redirect(url_for("monetize"))
    rows = db.query("SELECT * FROM requests WHERE to_id = ? ORDER BY created DESC", (me["id"],))
    requests_in = [decorate_request(r) for r in rows]
    accepted = [r for r in requests_in if r["status"] == "accepted"]
    earned = sum(r["amount"] for r in accepted)
    return render_template(
        "studio.html",
        requests=requests_in,
        pending=[r for r in requests_in if r["status"] == "pending"],
        earned=earned,
        fund=round(earned * FUND_SHARE),
        take_home=earned - round(earned * FUND_SHARE),
        experiences=listing_rows("experiences", member_id=me["id"]),
        artworks=listing_rows("artworks", member_id=me["id"]),
        posts=db.query("SELECT * FROM posts WHERE member_id = ? ORDER BY created DESC", (me["id"],)),
    )


@app.post("/studio/request/<int:rid>/<action>")
def decide_request(rid, action):
    me = current_member()
    row = db.query("SELECT * FROM requests WHERE id = ?", (rid,), one=True)
    if not me or not row or row["to_id"] != me["id"]:
        abort(403)
    status = "accepted" if action == "accept" else "declined"
    db.execute("UPDATE requests SET status = ? WHERE id = ?", (status, rid))
    flash(f"Request {status}.")
    return redirect(url_for("studio"))


@app.route("/studio/experience/new", methods=["GET", "POST"])
def new_experience():
    me = current_member()
    if not me or not me["monetized"]:
        return redirect(url_for("monetize"))
    if request.method == "POST":
        image = save_upload(request.files.get("image")) or request.form.get("image_url", "").strip()
        eid = db.execute(
            "INSERT INTO experiences (member_id, place_id, title, summary, details, price,"
            " duration, capacity, image, created) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (me["id"], int(request.form.get("place_id") or me["place_id"]),
             request.form.get("title", "Untitled").strip(),
             request.form.get("summary", "").strip(), request.form.get("details", "").strip(),
             int(request.form.get("price") or 0), request.form.get("duration", "2 hours").strip(),
             int(request.form.get("capacity") or 6), image, db.now()))
        flash("Experience listed.")
        return redirect(url_for("experience", eid=eid))
    return render_template("new_experience.html")


@app.route("/studio/art/new", methods=["GET", "POST"])
def new_artwork():
    me = current_member()
    if not me or not me["monetized"]:
        return redirect(url_for("monetize"))
    if request.method == "POST":
        image = save_upload(request.files.get("image")) or request.form.get("image_url", "").strip()
        aid = db.execute(
            "INSERT INTO artworks (member_id, place_id, title, medium, story, price, image,"
            " created) VALUES (?,?,?,?,?,?,?,?)",
            (me["id"], int(request.form.get("place_id") or me["place_id"]),
             request.form.get("title", "Untitled").strip(),
             request.form.get("medium", "").strip(), request.form.get("story", "").strip(),
             int(request.form.get("price") or 0), image, db.now()))
        flash("Piece listed.")
        return redirect(url_for("artwork", aid=aid))
    return render_template("new_artwork.html")


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    db.init()
    app.run(host="127.0.0.1", port=5000, debug=True)
