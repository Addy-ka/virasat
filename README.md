# Virasat

A club for people who are in love with a place.

Everyone here is the same kind of member. You write, photograph, paint, and copy out what the old
texts say. If you also want to sell an experience or a piece of your work, you turn selling on and a
dashboard appears inside the same site. No separate mode, no separate club for sellers.

Built with **Python (Flask) and HTML templates. There is no JavaScript anywhere in this project** —
every animation is CSS, and the theme switch is handled in Python.

## Run it

```powershell
cd Virasat
python -m pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

The database (`virasat.db`) builds itself on first run and fills with the starter content.
Delete that file to start over.

## Things to try

| As anyone | As a member who sells |
|---|---|
| Choose three or four places you love on the front page; the feed becomes those places, plus ones that share their character | Turn on selling from your profile, pick how you'd like to be paid, and a **Dashboard** appears in the top bar |
| Open a place: its photo gallery opens like a flower, each picture captioned with what it actually shows | Requests from members arrive there; accept or decline each one |
| Read what the old texts say, with the era, the language, where the manuscript survives, and how far it can be trusted | List an experience (your price, your hours, your group size) or a piece of work with its story |
| Post a story, photographs, a painting, a recipe or an old text, with pictures you upload | Watch what you have earned, and the share going to the place's preservation fund |
| Appreciate and respond to other members' posts | |
| Ask about an experience, or offer your own price for a piece of art | |

Sign in as any of the fourteen members (no passwords — it's a prototype). **Kamla Devi Prajapat**
sells, so her dashboard already has requests waiting.

## Where the money goes

A member keeps **90%** of anything they accept. The other **10%** goes to that place's preservation
fund. Virasat takes nothing. Account details are never collected or asked for in a message.

## The animation, without JavaScript

| What you see | How it is done |
|---|---|
| Opening curtain on the front page | a CSS `clip-path` animation that lifts itself away |
| Photographs that glide from a card into the next page's hero | the browser's view transitions, with matching `view-transition-name`s |
| Headings that lift word by word | Python's `words` filter wraps each word; CSS staggers them |
| The floral gallery opening as you reach it | rotated petals on a scroll-driven `animation-timeline: view()` |
| Rolling numbers on the front page | Python prints the digit columns; CSS slides each to its digit |
| Parallax heroes, reveals, flip cards, marquee, hover growth | CSS scroll timelines, transitions and `:hover` |
| Full-screen pictures | `:target`, a plain link to an id |

Anything the browser doesn't support simply doesn't animate; the page still reads correctly, and
`prefers-reduced-motion` turns the movement off.

## Files

| File | What's in it |
|---|---|
| `app.py` | Every page and form: the routes, the theme switch, uploads |
| `db.py` | The database: plain `sqlite3`, no ORM, the schema in one string |
| `seed_data.py` | Starter content: places, galleries with captions, old texts, members, posts, experiences, art |
| `templates/` | The pages. `base.html` is the shell, `_cards.html` holds the reusable pieces |
| `static/css/style.css` | All of the styling and all of the movement, dark and light |
| `static/uploads/` | Pictures members upload |

## Notes

- Members, requests and money are fictional. The places, crafts and old texts are real, and each
  text says plainly how well attested it is.
- Photographs come from Pexels (free licence), so the pages need an internet connection.
- Passages from old texts are paraphrased in plain English rather than quoted from a modern
  translation.
- Dark by default. The switch in the top bar is remembered for your session.
