import os
import re
import time
import trafilatura
from pathlib import Path

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────

UNCLEAN_DIR = "documents/raw_docs_unclean"
OUTPUT_DIR  = "documents/raw_docs"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

SOURCES = [
    {"id": 1,  "type": "reddit",  "url": "https://www.reddit.com/r/AskOldPeople/comments/1klq25w/women_who_solo_travelled_in_their_youth_what_was/"},
    {"id": 2,  "type": "reddit",  "url": "https://www.reddit.com/r/travel/comments/jswvex/solo_trip_tips_for_a_girl/"},
    {"id": 3,  "type": "reddit",  "url": "https://www.reddit.com/r/travel/comments/1sfuuek/solo_traveling_as_a_woman_is_it_actually_safe_or/"},
    {"id": 4,  "type": "reddit",  "url": "https://www.reddit.com/r/TheGirlSurvivalGuide/comments/18z2m9c/women_whove_gone_on_solo_trips_how_do_you_do_it/"},
    {"id": 5,  "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/b6t9z8/what_adviceprecautions_can_you_give_to_a_girl_in/"},
    {"id": 6,  "type": "reddit",  "url": "https://www.reddit.com/r/solofemaletravellers/comments/1qyhrv7/hi_ladies_please_share_your_first_solo_travel/"},
    {"id": 7,  "type": "reddit",  "url": "https://www.reddit.com/r/NeedTravelAdvice/comments/1rzpsaj/safest_countries_for_women_traveling_solo/"},
    {"id": 8,  "type": "reddit",  "url": "https://www.reddit.com/r/TooAfraidToAsk/comments/x9wze7/women_of_reddit_which_countrycity_would_you/"},
    {"id": 9,  "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/176xzs0/an_unfortunate_reminder_for_other_young_female/"},
    {"id": 10, "type": "blog",    "url": "https://www.roadscholar.org/travel-tips/solo-female-travel-for-women/"},
    {"id": 11, "type": "reddit",  "url": "https://www.reddit.com/r/solofemaletravellers/comments/1otb107/where_did_you_feel_surprisingly_safe_or_unsafe_as/"},
    {"id": 12, "type": "reddit",  "url": "https://www.reddit.com/r/TwoXChromosomes/comments/1da7j9w/how_do_you_solo_female_travelers_manage_to_feel/"},
    {"id": 13, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/1bx1mfz/solo_travel_as_a_senior_woman/"},
    {"id": 14, "type": "reddit",  "url": "https://www.reddit.com/r/travel/comments/19ar3r6/is_solo_traveling_as_a_woman_as_dangerous_as_its/"},
    {"id": 15, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/12b3gff/solo_female_travelers_how_do_you_get_over_the/"},
    {"id": 16, "type": "reddit",  "url": "https://www.reddit.com/r/AskWomen/comments/ax57cz/solo_traveling_ladies_of_reddit_how_did_you_come/"},
    {"id": 17, "type": "reddit",  "url": "https://www.reddit.com/r/travel/comments/x6xx4c/the_advice_i_needed_3_years_ago_when_i_started/"},
    {"id": 18, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/fc9vd7/i_consolidated_all_of_rsolotravels_little_hacks/"},
    {"id": 19, "type": "blog",    "url": "https://solotravelerworld.com/category/how-to-travel-alone/solo-female-travel/"},
    {"id": 21, "type": "blog",    "url": "https://blondwayfarer.com/beginners-guide-solo-female-travel/"},
    {"id": 23, "type": "reddit",  "url": "https://www.reddit.com/r/AskWomenOver60/comments/1fdunkm/if_you_travel_solo_do_you_feel_more_vulnerable_as/"},
    {"id": 24, "type": "blog",    "url": "https://thegoodlifeabroad.com/senior-women-travel/auto-draft"},
    {"id": 25, "type": "blog",    "url": "https://www.women-on-the-road.com/solo-travel.html"},
    {"id": 26, "type": "article", "url": "https://thecatalystnews.com/2025/10/24/the-benefits-and-pitfalls-of-solo-female-travel/"},
    {"id": 27, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/d9ripx/its_okay_to_discuss_the_negatives_of_solo_travel/"},
    {"id": 28, "type": "blog",    "url": "https://www.wheregoesrose.com/pros-cons-solo-travel/"},
    {"id": 29, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/171ihf6/attention_solo_women_travellers_please_read_this/"},
    {"id": 30, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/k166cm/experiences_of_black_women_traveling_solo_in_italy/"},
    {"id": 31, "type": "reddit",  "url": "https://www.reddit.com/r/blackladies/comments/11f7m8z/honest_advice_from_black_girls_who_like_to_travel/"},
    {"id": 32, "type": "reddit",  "url": "https://www.reddit.com/r/blackladies/comments/xonkxj/international_solo_travel_how_do_you_enjoy_travel/"},
    {"id": 33, "type": "reddit",  "url": "https://www.reddit.com/r/solotravel/comments/6dluxu/solo_travelling_concerns_asian_female/"},
    {"id": 34, "type": "blog",    "url": "https://adventureswithcarli.com/resources/solo-travel/safety-tips-for-solo-travelers/"},
    {"id": 35, "type": "article", "url": "https://www.essence.com/lifestyle/travel/solo-travel-tips-for-beginners/"},
    {"id": 36, "type": "blog",    "url": "https://www.bucketlistly.blog/posts/solo-female-traveler-gone-goat-interview"},
    {"id": 37, "type": "blog",    "url": "https://eatwanderexplore.com/start-traveling-blog/is-it-safe-for-women-or-lgbtq-to-travel-around-the-world-plus-expert-travel-advice"},
]

# ─────────────────────────────────────────
# CLEAN REDDIT (from pasted .txt files)
# ─────────────────────────────────────────

def clean_pasted_reddit(text: str) -> str:
    # preserve the header (SOURCE_ID, SOURCE_TYPE, URL, ===)
    header = ""
    content = text
    if "======" in text:
        parts = text.split("=" * 60)
        header = parts[0] + "=" * 60 + "\n\n"
        content = parts[1] if len(parts) > 1 else text

    # strip everything above Comments Section in the content
    content = re.sub(r'^.*?Comments Section\n', '', content, flags=re.DOTALL)
    # strip Reddit footer
    content = re.sub(r'Reddit Rules.*$', '', content, flags=re.DOTALL)
    # remove upvote/downvote/reply lines
    content = re.sub(r'\n(Upvote|Downvote|Reply|Share|Report|Save|Follow|Join the conversation|Sort by:|Search Comments|Expand comment search)\s*\n', '\n', content)
    content = re.sub(r'\nUpvote\s+\d+\s+Downvote\n', '\n', content)
    # remove standalone vote counts
    content = re.sub(r'\n\d+\n', '\n', content)
    # remove age tags
    content = re.sub(r'\n(MOD|AUTO|[0-9]+ something|Old)\n', '\n', content)
    # remove timestamps
    content = re.sub(r'•?\s*\d+[ymd] ago', '', content)
    # remove usernames
    content = re.sub(r'\nu/\S+\s*\n', '\n', content)
    # remove avatar lines
    content = re.sub(r'\S+ avatar\n', '', content)
    # remove edited notices
    content = re.sub(r'•?\s*Edited \d+[ymd] ago', '', content)
    # remove [deleted]
    content = re.sub(r'\[deleted\]\n', '', content)
    # collapse whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    # remove AutoModerator line
    content = re.sub(r'AutoModerator\n', '', content)
    # remove standalone usernames (lines with no spaces, just a username)
    content = re.sub(r'\n[A-Za-z0-9_-]+\n', '\n', content)
    # remove bare "Reply" lines
    content = re.sub(r'\nReply\n', '\n', content)
    # remove bullet points
    content = re.sub(r'\n•\n', '\n', content)

    return (header + content.strip())

def process_reddit_file(doc_id: int) -> bool:
    """Find and clean a pasted reddit file from raw_docs_unclean."""
    # look for any file matching doc_XX_reddit_raw.txt or doc_XX_reddit.txt
    patterns = [
        f"doc_{doc_id:02d}_reddit_raw.txt",
        f"doc_{doc_id:02d}_reddit.txt",
        f"doc_{doc_id}.txt",
    ]
    found_path = None
    for pattern in patterns:
        path = os.path.join(UNCLEAN_DIR, pattern)
        if os.path.exists(path):
            found_path = path
            break

    if not found_path:
        print(f"  ✗ No file found in {UNCLEAN_DIR}/ for doc {doc_id:02d} — skipping")
        return False

    with open(found_path, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_pasted_reddit(raw)
    out_path = f"{OUTPUT_DIR}/doc_{doc_id:02d}_reddit.txt"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"  ✓ Cleaned → {out_path}  ({len(cleaned):,} chars)")
    return True


# ─────────────────────────────────────────
# FETCH BLOGS + ARTICLES (trafilatura)
# ─────────────────────────────────────────

def fetch_article(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        no_fallback=False
    )
    text = re.sub(r'^- ', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^.+\|\s*By\s+.+$', '', text, flags=re.MULTILINE)
    return text or ""


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

failed = []

for source in SOURCES:
    doc_id   = source["id"]
    doc_type = source["type"]
    url      = source["url"]

    print(f"[{doc_id:02d}] Processing {doc_type}...")

    try:
        if doc_type == "reddit":
            process_reddit_file(doc_id)

        else:
            filename = f"{OUTPUT_DIR}/doc_{doc_id:02d}_{doc_type}.txt"
            cleaned  = fetch_article(url)

            if not cleaned:
                print(f"  ✗ Empty content — skipping")
                failed.append((doc_id, url, "Empty content"))
                continue

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"SOURCE_ID: {doc_id}\n")
                f.write(f"SOURCE_TYPE: {doc_type}\n")
                f.write(f"URL: {url}\n")
                f.write("=" * 60 + "\n\n")
                f.write(cleaned)

            print(f"  ✓ Saved → {filename}  ({len(cleaned):,} chars)")
            time.sleep(2)

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        failed.append((doc_id, url, str(e)))

# ─────────────────────────────────────────
# SPOT CHECK
# ─────────────────────────────────────────

print("\n" + "=" * 60)
print("SPOT CHECK — first reddit file (first 2000 chars)")
print("=" * 60)

for f in sorted(os.listdir(OUTPUT_DIR)):
    if "reddit" in f:
        with open(f"{OUTPUT_DIR}/{f}", "r", encoding="utf-8") as fh:
            print(fh.read(2000))
        break

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────

print("\n" + "=" * 60)
total     = len(SOURCES)
succeeded = total - len(failed)
print(f"Done: {succeeded}/{total} processed")

if failed:
    print(f"\nFailed ({len(failed)}):")
    for doc_id, url, err in failed:
        print(f"  [{doc_id:02d}] {url[:60]} — {err}")