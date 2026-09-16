# Virasat

**A club for people who are in love with a place.**

Virasat is a place-first community site. Members share stories, photographs, paintings, recipes
and passages from old texts about the places they love. Anyone who wants to can also offer an
experience or sell a piece of their work, and manage requests and earnings from a dashboard
inside the same site.

**Live demo: https://virasat-3s83.onrender.com**

> The demo runs on a free server that sleeps when idle, so the first visit can take about a minute
> to load. It resets from time to time; anything you post there is temporary.

## What's inside

- **Start with places you love.** Pick up to four places and the home feed becomes their stories,
  experiences and art, plus places that share their character.
- **Place pages** with a floral photo gallery, the old texts the place appears in, what members are
  posting and offering, and who is there.
- **A library of old texts**, each with its era, language, where it survives, and an honest note on
  how reliable it is.
- **One kind of member.** Everyone can post. Selling is an optional switch that adds a dashboard for
  requests and earnings.
- **Transparent money.** Sellers set their own price and keep 90%; 10% goes to that place's
  preservation fund.
- **Dark and light themes**, dark by default.

Places in the demo: Jaipur, Varanasi, Kutch, Kochi, Ladakh and Hampi.

## Built with

- Python 3 and [Flask](https://flask.palletsprojects.com/)
- Jinja templates and SQLite
- Plain CSS for all animation: view transitions, scroll-driven effects and keyframes.
  There is no JavaScript in the project.

## Run it locally

```bash
git clone https://github.com/Addy-ka/virasat.git
cd virasat
python -m pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000. On Windows you can double-click `run.bat` instead.

The SQLite database is created and filled with demo content on first run.

## Project structure

```
app.py              routes, forms, uploads, theme switch
db.py               SQLite schema and helpers
seed_data.py        demo content: places, galleries, old texts, members, posts, listings
templates/          page templates (_cards.html holds shared components)
static/css/         the stylesheet, including every animation
static/uploads/     images uploaded by members
render.yaml         deployment config for Render
```

## About the content

The places, crafts and old texts are real. Passages from old texts are paraphrased in plain
English, and each one notes its source and how far it can be trusted.

The members, posts, requests and payments are fictional demo data.

Photographs are from [Pexels](https://www.pexels.com) and used under the Pexels licence.
