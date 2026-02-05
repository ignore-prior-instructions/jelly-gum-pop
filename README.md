# ✨🦄💖 jellygumpop.party 💿🌈🛼

✨🦄💖 a glitter-soaked django app that poofs quizzes out of thin air and yeets the results across the internet 💿🌈🛼

---

## what is this

this is a tiny, unserious web app where:

- someone writes **one prompt**
- a quiz magically appears
- friends take it
- everyone shares their extremely important results

that's it.  
no builders. no dashboards. no dignity.

---

## the basic idea (brain version)

- quizzes are generated from a **single LLM prompt**
- each quiz is stored as a **simple JSON blob**
- quizzes are fetched by **ID**
- taking a quiz produces a **shareable result page**
- result pages are also fetched by **ID**
- everything is designed to be:
  - fast  
  - cheap  
  - disposable  
  - extremely shareable  

this is not a platform.  
this is an internet object.

---

## vibes & rules

- creation should feel like **pressing a button**
- editing is allowed, but only as "nudge it again"
- quizzes are always playable
- results should feel confident, even when wrong
- if it takes longer than ~90 seconds end-to-end, something is broken
- tone > accuracy
- fun > polish
- shipping > thinking

---

## what this is built with

- django (kept intentionally minimal)
- server-rendered pages
- JSON-first quiz storage
- LLM backends: **anthropic claude** or **openai gpt-4o** (your choice!)
- no required auth
- no required accounts
- future-you *can* add those later if you really must

---

## what this is not

- a quiz builder
- a CMS
- a serious personality test
- a labrat thing
- a startup pitch
- a responsible use of time

---

## running it

good news! it exists now ✨

```bash
# install dependencies
pip install -r requirements.txt

# set up your API key (choose one or both!)
cp .env.example .env
# edit .env and add either:
#   ANTHROPIC_API_KEY (for Claude)
#   OPENAI_API_KEY (for GPT-4o)
# or both! it'll auto-detect which one to use
#
# optional: use a custom OpenAI-compatible endpoint
#   OPENAI_BASE_URL=https://your-endpoint.com/v1

# run migrations
python manage.py migrate

# start the server
python manage.py runserver
```

then open `http://localhost:8000` and start poofing quizzes into existence

### optional: create an admin user

```bash
python manage.py createsuperuser
```

then visit `http://localhost:8000/admin` to see all your quizzes and results

---

## final note

if this ever feels too polished, too serious, or too "product-y":

✨ **you've gone too far** ✨

turn the knob back up. add more glitter. ship anyway.

🦄💖🌈
