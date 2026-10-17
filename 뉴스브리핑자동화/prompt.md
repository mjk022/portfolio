# Morning brief 프롬프트 (개인 식별 정보 제거본)

claude.ai 예약 루틴에 등록된 지시문 원문입니다.<br>
아티팩트 주소, Notion 페이지·데이터베이스 ID는 `<...>` 자리표시자로 바꿨습니다.

```text
Make today's morning brief for me. Publish it by updating my existing brief artifact in place, save a copy of today's cards into the artifact's database, AND add it as a new page in my Notion database, AND add any new AI terms/services to my Notion AI dictionary, AND put a table of today's AI terms at the very end of today's Notion page. Do not send any email.

Language: Korean (한국어). Write everything in Korean.
Home timezone: Asia/Seoul. "Today" means today's date in Asia/Seoul.

CORE RULE — organise by TOPIC, never by source. News sites, X posts and YouTube videos are all just inputs. Merge them into topic sections. Do not make sections like "X에서 본 소식" or "유튜브 새 영상". When an X post or a video is about the same story as a news card, fold it into that card: add a sentence to the card text and an extra source link. Otherwise give it its own card in the matching topic.

TEMPLATE — the layout is fixed:
1. Read the artifact <BRIEF_ARTIFACT_URL> with the Artifact tool (action "read"). Its HTML is the template. Keep its <style>, structure, ids, class names and the whole <script> exactly as they are (the script includes the ask box's web search tool — keep it). Keep the date bar <nav class="band daynav" id="daynav" ...><div class="wrap" id="daylist"></div></nav> unchanged and keep id="topwrap" on the top band's inner div. The script runs the date bar (switching between saved daily briefs), the card rails and the "브리핑에 대해 물어보기" ask box (id="ask"). Keep everything inside the ask section unchanged except the three .sug buttons: the .sub line, the conversation log (#log, #logbar), #notice, the photo and file attach buttons (#photoBtn, #attach, #photo, #file), #chips, #fhint, #stat and the hidden #past block. The script keeps each day's Q&A separate and reads today's date from the .date line, so the .date line must keep the format "요일 · YYYY년 M월 D일". Replace only the brief content (date line, headline, note, cards, .sug buttons).
2. Republish to that same url with capabilities {"sample": {}, "db": {}, "user": {}, "mcp": {"servers": [{"server": "Apify", "tools": ["apify--rag-web-browser", "get-actor-run", "get-dataset-items"]}]}} so the ask box (including its web search through the Apify connector), attachments, saved briefs and saved conversations keep working. Never drop db, user or mcp. Do not pass `contract`. Do not pass `files` (the tess/ files for photo text reading are already published and must stay). Do not create a new artifact.
3. Right after publishing, save today's brief into the artifact's database so it can be reopened later from the date bar: write a local JSON file with {"date": "YYYY-MM-DD", "top": <the inner HTML of div#topwrap>, "secs": <the outer HTML of every section.sec, joined with "\n">, "sugs": <the inner HTML of #sugs>, "savedAt": <current time in ms>}, then call the ArtifactData tool with action "set", url <BRIEF_ARTIFACT_URL>, collection "briefs", doc_id = today's date (YYYY-MM-DD), file_path = that JSON file. If the document already exists, read it first and pass its version as if_version. Never touch any "data/users/..." documents.

Page content:
- Top band: the day-date line for TODAY (e.g. "월요일 · 2026년 10월 5일"), and a one-line serif headline addressed to me about the shape of the day. If a calendar connector (Google Calendar or Outlook) is connected, draw today's meetings on the terrain SVG (one stroke, elevation = meeting load, dots for meetings) and replace the note under the drawing with a short sentence about the day; if no calendar is connected, keep the flat line and the existing note. Use the morning skill (anthropic-skills:morning) only for its guidance on the headline and terrain. Ignore its "no cards" rule, because this page is card news on purpose.
- Topic sections, each a horizontal card rail, in this order:
  • AI·테크: about 6–9 cards covering BOTH AI and wider technology: new AI models and products, chips and semiconductors, big tech, EVs and autonomous driving, robots, space, smartphones and gadgets. Always include the day's most talked-about tech story even when it is not AI (for example a viral product reveal like Tesla's flying Roadster); run a web search for the day's trending tech news (e.g. "오늘 화제 테크 뉴스", "trending tech news") to find it. Do NOT make cards about corporate donations, grants, funds, fellowships, free-access or sponsorship programs, or similar PR/philanthropy announcements. Include relevant X posts and noteworthy AI videos. You may group 2–3 non-news AI videos into one "이번 주 볼만한 AI 영상" card with several links.
  • 경제·시장: about 5–6 cards, e.g. KOSPI/KOSDAQ close, USD/KRW, Korean export or macro data, US market close and notable movers, US data and Fed expectations, oil and commodities. Note market holidays and the next trading day when relevant. The 오선의 미국 증시 라이브 daily-summary video, when there is one, is attached to the US market card as an extra link.
  • 세계 경제: exactly 2 cards (always include this section) on the world economy beyond Korea and the US stock market, e.g. IMF / World Bank / OECD outlooks, China, Japan, Europe, emerging markets, global trade, central banks abroad (ECB, BOJ, PBOC), currencies and gold. Same card format with a key-figure box. Prefer primary sources (IMF, national statistics offices, central banks) or major wires, and end each card with why it matters for Korea. Do not repeat a story already covered in 경제·시장.
  • 국내·북한: 3–4 Korea and North Korea headlines. This is the "short" section: stacked cards with no key-figure box, and 1–2 sentences each.
  If one day has a strong story in another topic (e.g. 국제), you may add a section for it with the same card format, placed after 세계 경제 and before 국내·북한.
- Card format (keep the classes from the template):
  • .tag = the topic name
  • .cnt = "n / total"
  • a key-figure box (.key with .kv as the big number or short term, .kl as a short label), skipped in the short section. If .kl mentions a number that is not today's news (e.g. an earlier funding round), say in the card text where it came from and when.
  • a short Korean title in my own words (h3, also put in data-title)
  • about 4 sentences (.txt) for news cards: what happened, with concrete numbers, names and dates, then the background, then why it matters for Korea or for me
  • .foot > span.srcs holding one or more <a class="src">outlet ↗</a> links. Name the source naturally, e.g. "아시아경제 시황", "X @Reuters", "영상 오선".
- Update the three suggested-question buttons (.sug) so they fit today's news.
- Use web search and open the source articles for the facts. State only what the sources say. If sources disagree, prefer closing figures. For videos, say only what the title and description show. Drop a card rather than guess.
- Escape all fetched text as plain text in the HTML.

Inputs to gather (all via the Apify connector, plus web search):
- X: call Apify actor "xquik/x-tweet-scraper" with call-actor, input {"twitterHandles": ["OpenAI","AnthropicAI","GoogleDeepMind","karpathy","TechCrunch","Reuters","business","WSJmarkets","FirstSquawk"], "maxItemsPerTarget": 8, "maxItems": 72}, callOptions {"maxTotalChargeUsd": 0.1}. Read the dataset with get-dataset-items, using fields createdAt,author.username,text,url,likeCount,isRetweet,isReply. Use original posts (not replies, not retweets) from the last ~36 hours. Skip ads, event promos and podcast plugs.
- YouTube: call Apify actor "grow_media/youtube-channel-video-scraper" with input {"channelUrls": ["https://www.youtube.com/@futuresnow","https://www.youtube.com/@jocoding","https://www.youtube.com/@aiexplained-official","https://www.youtube.com/@TwoMinutePapers","https://www.youtube.com/@matthew_berman"], "maxResults": 3, "videoType": "long", "sortOrder": "latest"} (videoType must be "long"), callOptions {"maxTotalChargeUsd": 0.1}. Read the dataset with fields channelName,title,date,viewCount,duration,url,description. Use videos from the last ~48 hours, widening to 7 days for AI videos if needed.
- If either Apify call fails, continue with web news only.

Notion step (Notion connector), done after the artifact is published:
- Add one new page to my "브리핑 기록" database, data source collection://<NOTION_DATA_SOURCE_ID> (database <NOTION_PAGE_URL>, inside my "아침 브리핑" page). Use notion-create-pages with parent {"type":"data_source_id","data_source_id":"<NOTION_DATA_SOURCE_ID>"} and icon "☀️". If a page for today's date already exists in that database, update it instead of adding a duplicate.
- Properties:
  • "제목": e.g. "10월 5일 (월) 아침 브리핑"
  • "date:날짜:start": today's date as YYYY-MM-DD, with "date:날짜:is_datetime": 0
  • "한줄 요약": one Korean line with the day's 2–3 biggest items
  • "키워드": a JSON array chosen from ["AI","경제","증시","국내","X","정치"]
- Content, in Notion-flavored markdown. Escape special characters such as $ ~ [ ] < > with a backslash in plain text. Use the reference page <NOTION_PAGE_URL> as the layout example (fetch it). The layout, top to bottom:
  1. A yellow_bg callout with icon ☀️. Its first line is "**<headline>**" plus one short sentence. Its second line is the links [📱 카드뉴스로 보기 · 질문하기](<BRIEF_ARTIFACT_URL>) · [📚 AI 용어·서비스 사전](<NOTION_PAGE_URL>).
  2. A gray_bg callout with icon ⚡ holding "**30초 요약**" and 4–5 short bullets. Each bullet is one line on one of the day's biggest items.
  3. "### 📊 오늘의 숫자", then a <table header-row="true" fit-page-width="true"> with FOUR columns: 지표 / 값 / 변동 / 기준. Rows: 코스피, 코스닥, 원·달러, 나스닥, S&P 500, WTI, plus any other key number of the day. The 기준 column always says exactly which date and what comparison the change refers to, e.g. "10/2(목) 종가 · 전일 대비", "10/2(목) 오후 3:30 · 전일 대비", "미국 10/2(금) 종가 · 전일 대비", "10/1 발표 · 작년 9월 대비". Use the actual last trading day for each market; after a holiday or weekend, it's the last session. Colour changes Korean-style: rises <span color="red">, falls <span color="blue">.
  4. A plain callout with icon 👆 saying "제목을 누르면 내용이 펼쳐져요."
  5. Topic sections, the same as the card page and in the same order: "## 🤖 AI·테크", "## 📈 경제·시장", "## 🌐 세계 경제", then any extra topic (e.g. "## 🌍 국제"), then "## 🇰🇷 국내·북한". Each card is a toggle heading: "### <title> · <span color="orange"><kv></span> {toggle="true"}". Add the orange figure only when kv is a number that isn't already in the title. In the short section, use the title alone. Under each toggle heading, indented with one tab, put:
     • a gray line with "<kv> · <kl>" (skipped in the short section)
     • the card text
     • one line with all its sources, "[<source> ↗](<url>) · [<source> ↗](<url>) {color="gray"}"
  6. A divider "---", then a blue_bg callout with icon 💬. It holds three lines: "**궁금한 게 있으면 물어보세요**", the link [💬 브리핑에 대해 물어보기 →](<BRIEF_ARTIFACT_URL>#ask), and the gray line <span color="gray">카드 페이지의 질문창으로 바로 가요. Claude 앱이나 claude.ai에서 열면 질문할 수 있어요.</span>
  7. LAST on the page: "### 📚 오늘 나온 AI 용어" and its table — added in the AI dictionary step below with insert_content at the end of the page.
  • Use the same text as the cards.
- If Notion is unavailable, skip this step and still publish the artifact.

AI dictionary step (Notion connector), done after today's brief page exists:
- My "AI 용어·서비스 사전" database is <NOTION_PAGE_URL>, data source collection://<NOTION_DATA_SOURCE_ID>. It is a table of named AI things that show up in my briefs, e.g. Muse Spark (Meta의 헬스케어 AI), Mythos (보안 프로그램 약점 찾는 AI 모델), 구글 버그바운티 (보안 약점 찾으면 보상). Fetch the data source first to see its current properties, and only fill properties that exist.
- The dictionary page has a last view tab "🧠 AI 모델 정리" that lists every row whose 분야 contains "AI 모델", newest 발표일 first. It updates itself from the rows. Whenever an item is an AI model, model version or model family (e.g. Claude Haiku 5.5, Gemini 4 Argon, Beam), always include "AI 모델" in its 분야 (alongside any other fitting tag) and fill 발표일 when a source states it, so it shows up correctly there. Never change, reorder or delete the database's views.
- From today's brief (all topics, plus any X posts or videos you used), list every NAMED AI-related thing: a model, product, service, device, feature, research project, program (e.g. bug bounty), campaign, policy/regulation, or new term. Skip generic words (AI, LLM, 반도체), company names on their own, and non-AI tech products.
- Query the data source to get the existing rows (이름, url). Treat different spellings or Korean/English versions of the same thing as the same entry.
- For each NEW item, create a page with notion-create-pages, parent {"type":"data_source_id","data_source_id":"<NOTION_DATA_SOURCE_ID>"}, properties:
  • "이름": the official name (add Korean in parentheses if helpful)
  • "한줄 설명": 1–2 Korean sentences, plain words: what it is, what it does, and one concrete fact (number, price, date, availability)
  • "분야": a JSON array from ["AI 모델","보안","헬스케어","하드웨어·인프라","정책·규제","연구","서비스·기기","캠페인"]
  • "회사·기관": the company or organisation
  • "date:발표일:start": the announcement/release date as YYYY-MM-DD (with "date:발표일:is_datetime": 0), only if a source states it; otherwise leave it empty
  • "출처": the URL of the best primary source (official blog/announcement first, otherwise the main news article you used)
  • "추가 출처": a second source URL, if there is one
  • "관련 브리핑": a JSON array with today's brief page URL, e.g. ["<NOTION_PAGE_URL>"]
- For each item that ALREADY exists, fetch that row and add today's brief page to its "관련 브리핑" relation (keep the existing relations). If today's news adds an important new fact, update "한줄 설명" too. If an existing AI-model row is missing "AI 모델" in 분야, add it.
- Only state what the sources say. If you can't find a reliable source link for an item, skip it.
- Then append the table to the very end of today's brief page with notion-update-page, command "insert_content", position {"type":"end"} (after the 💬 callout). Format:
  "### 📚 오늘 나온 AI 용어", then <table header-row="true" fit-page-width="true"> with THREE columns: 용어 / 한 줄 뜻 / 출처. One row per item from today's brief (new and already-existing ones), biggest news first. 용어 = a page mention of that dictionary row (<mention-page url="..."/>). 한 줄 뜻 = a very short plain Korean phrase (max ~40 characters). 출처 = "[<source> ↗](<url>)". Copy the exact format from the end of the reference page <NOTION_PAGE_URL>.
- If today's brief has no named AI items, skip the table.

This is an unattended scheduled run. Do not ask questions or suggest connectors. Before publishing, check once that the page renders: take one screenshot with Playwright using executablePath '/opt/pw-browsers/chromium', at a width of 400px, and confirm there is no horizontal page scroll. Then publish, save the brief copy, add the Notion page, update the AI dictionary and the 오늘 나온 AI 용어 table, and reply with one line summarizing the day (mention how many dictionary entries were added).
```
