# The Unofficial Guide — Project 1

---

## Domain

My domain is solo female travel experiences. This unofficial guide will provide general information, spanning what it’s like to travel at different ages as a woman, the pros and cons of solo travel, and packing and safety advice. This knowledge is hard to find because it’s spread across diverse sources. It’s time-consuming to go through each source, and there’s a high likelihood you'll miss key information while searching for what you need about solo female travel experiences. 
---

## Document Sources


| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/AskOldPeople | A thread of women solo travel experiences in their youth | [Link](https://www.reddit.com/r/AskOldPeople/comments/1klq25w/women_who_solo_travelled_in_their_youth_what_was/) |
| 2 | r/travel | Solo trip tips for girls | [Link](https://www.reddit.com/r/travel/comments/jswvex/solo_trip_tips_for_a_girl/) |
| 3 | r/travel | Whether or not solo traveling is safe for women | [Link](https://www.reddit.com/r/travel/comments/1sfuuek/solo_traveling_as_a_woman_is_it_actually_safe_or/) |
| 4 | r/TheGirlSurvivalGuide | Advice from women who've gone on solo trips | [Link](https://www.reddit.com/r/TheGirlSurvivalGuide/comments/18z2m9c/women_whove_gone_on_solo_trips_how_do_you_do_it/) |
| 5 | r/solotravel | Safety precautions and advice for girls in twenties | [Link](https://www.reddit.com/r/solotravel/comments/b6t9z8/what_adviceprecautions_can_you_give_to_a_girl_in/) |
| 6 | r/solofemaletravellers | Solo female travel experiences | [Link](https://www.reddit.com/r/solofemaletravellers/comments/1qyhrv7/hi_ladies_please_share_your_first_solo_travel/) |
| 10 | Road Scholar | Solo Travel Guide for Women | [Link](https://www.roadscholar.org/travel-tips/solo-female-travel-for-women/) |
| 21 | Blond Wayfarer | Solo Female Travel Guide for Beginners | [Link](https://blondwayfarer.com/beginners-guide-solo-female-travel/) |
| 26 | The Catalyst | Benefits and Pitfalls of Solo Female Travel | [Link](https://thecatalystnews.com/2025/10/24/the-benefits-and-pitfalls-of-solo-female-travel/) |
| 34 | Adventures with Carli | Safety tips for solo travelers | [Link](https://adventureswithcarli.com/resources/solo-travel/safety-tips-for-solo-travelers/) |
| 35 | Essence | The Black girl's guide to traveling internationally | [Link](https://www.essence.com/lifestyle/travel/solo-travel-tips-for-beginners/) |
| 37 | EatWanderExplore | Advice for solo female and LGBTQ traveling | [Link](https://eatwanderexplore.com/start-traveling-blog/is-it-safe-for-women-or-lgbtq-to-travel-around-the-world-plus-expert-travel-advice) |

---

## Chunking Strategy

Since I have diverse sources, I plan to split each source type differently. 

| Source | Chunk Size | Overlap Size |
|--------|------------|--------------|
| Reddit | 400 Characters | 50 Chars |
| Blogs | 1000 Characters | 100 Chars|
| Articles | 1000 Characters | 100 Chars |

**Reasoning:**
Reddit: Reddit posts and comments are of shorter length generally. 
Articles and Blogs: Both forms of sources are longer and narrative like, and organized by topic. 

I'm planning to mainly implement recursive chunking to split text. Reddit posts aren't uniformly sized and tend to have noisy unstructured text. Recursive chunking also can be used for articles and blogs since they may not have consistent formattings.

Finalized:
| Source | Chunk Size | Overlap Size |
|--------|------------|--------------|
| Reddit | 400 Characters | 50 Chars |
| Blogs | 550 Characters | 100 Chars|
| Articles | 500 Characters | 100 Chars |

After implementing chunk.py, I realized the chunks for blogs and articles are too lengthy and involved noisy/irrelevant information. So I cut it short around 500-550 for blogs and articles. 

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence transformers

**Production tradeoff reflection:**
I would weigh in context length and latency when it comes to choosing a different embedding model. I think the current model is quite lengthy and verbose. 

---

## Grounded Generation

**System prompt grounding instruction:** I instructed it to enforce grounding and not just suggest it. I also prompt Claude to ensure that attribution is guaranteed in the program.

**How source attribution is surfaced in the response:** In the response, the source is cited as [source #]. And below the response, the user can see the metadata associated with it. 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are people's opinions about staying in hostels as a solo female traveler? | People say staying in hostels feel safe and gives a sense of community. Plus it is budget friendly | "People generally have positive opinions about staying in hostels as a solo female traveler. For example, one traveler mentions that they "love the frugality + potential community of hostels" and haven't had any negative experiences, aside from usual annoyances like noise [Source 1]. Another traveler notes that hostels are "generally pretty good for meeting people if you make use of the common areas" [Source 4]. It's also suggested that staying in female-only dorms can make solo female travelers feel more comfortable [Source 1]. Additionally, hostels often organize social events like pub crawls and day trips, making it easy to meet other travelers [Source 3]. However, it's recommended to choose well-reviewed hostels that are centrally located and safe [Source 2]." | Relevant | Accurate |
| 2 | What do people say about the pros of solo travel? | Self-development, empowerment, not waiting for people, complete control, managing own budget | "People say that solo travel is "much funner and more fulfilling" compared to traveling with friends, as it allows them to do what they want without considering others' needs [Source 1]. They also enjoy the freedom of not having to worry about other people's needs or getting lost and upsetting others, and instead like wandering around on their own [Source 2]. Additionally, solo travel is seen as a great learning experience, where one can learn more about themselves and the world around them [Source 3]. The ability to make small decisions and do whatever they want is also considered "so freeing" [Source 4]." | Relevant | Accurate |
| 3 | What do people say about managing to feel safe during traveling? | Being situationally aware, looking confident, and do your research | "According to [Source 2], to stay safe while traveling solo, especially as a woman, it's recommended to share your itinerary with friends or family and check in regularly, research your destination and hotels prior to traveling, have working cell phone data for international trips, and trust your instincts with new people and places. [Source 3] also advises to develop a sense of who you can trust and who might harm you, and not to feel pressured into something if it feels off. Additionally, [Source 4] suggests that solo traveling as a woman can be safe if you're not trying to go to an obviously unsafe area. [Source 1] mentions that even if things go wrong, you can still enjoy your trip and that worrying about danger is location dependent." | Relevant | Accurate |
| 4 | Why do people worry about traveling alone as a woman? | Safety Issues| "People worry about traveling alone as a woman because it can be an "uneasy experience" [Source 1] and can also be "nerve-wracking and, in some cases, unsafe" [Source 2]. Single women traveling alone share many of the same concerns [Source 1]." | Relevant | Accurate |
| 5 | How should one pack for a solo trip? | Pack lightly and stick to essentials| "To pack for a solo trip, it is advised to pack as lightly as possible [Source 1]. This means avoiding overpacking and sticking to essentials [Source 1]. A small rolling bag and a backpack are recommended, rather than two big suitcases, as they are easier to handle when traveling alone, such as when hopping aboard a train [Source 1]. It's also suggested to pack light, with a 30L backpack being a good target [Source 4], and to leave room for a few items you may need or want to buy [Source 4]. Additionally, traveling when it's warm can help, as you can wear less or lighter clothes [Source 4]." | Relevant | Accurate

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** Failure Case: The output to one question: "Should I go to Egypt" resulted in improper capitalization when quoting. This is likely due to improper cleaning of text. 

**What the system returned:**
"According to [Source 1], the author is not a fan of traveling to areas with high tourism levels, such as Egypt, due to the risk of being overcharged or swindled. They mention that "if you are going to a city or country with a high tourism level, such as Rome or Egypt, you'll get soaked." However, they do acknowledge that "The Pyramids are cool", suggesting that Egypt may have some attractions worth visiting. [Source 2] does mention that the author has traveled to "Most of Africa", which would include Egypt, but does not provide specific advice on traveling to Egypt. [Source 3] and [Source 4] do not mention Egypt at all."

**Root cause (tied to a specific pipeline stage):** Loading and Cleaning Pipeline

**What you would change to fix it:** Ensure proper capitalization in the loading and cleaning up pipeline

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Spec helped me decide on what tools to use and strategies to implement so that during the actual execution part, I was able to test and debug. For instance: By being able to decide the chunking size early on, I didn't need to think about it a lot during the implementation. I'd just execute it, see the results, and then refine it from there.

**One way your implementation diverged from the spec, and why:**
I ended up having to manually copy and paste reddit posts for 6 out of the 25 I listed in the planning.md. This is due to issues with accessing the posts since I was constantly being blocked. 
---

## AI Usage


<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude instructions on loading and cleaning documents from urls with my document section from planning.md. 
- *What it produced:* It returned a function that scraps reddit and blog as if they were the same type
- *What I changed or overrode:* I overrode it and emphasized the distinction between the two sources. 

**Instance 2**

- *What I gave the AI:* I gave Claude my architecture diagram, retrieval and evaluation sections from planning.md to develop the embed script with sentence transformers.  
- *What it produced:* It returned a function with a top_k of 5. 
- *What I changed or overrode:* I overrode it with 4 because the chunks had loosely related information. 
