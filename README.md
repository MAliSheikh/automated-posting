# Automated Multi-Platform Posting System

A FastAPI application that takes one short message and publishes it to **5 platforms** at the same time: Facebook, Instagram, Threads, Dev.to and Bluesky.

If one platform fails, the others still post. Every platform returns its own result (status, URL, date, time, error).

---

## Table of Contents

1. [Features](#features)
2. [Platforms Used](#platforms-used)
3. [Project Structure](#project-structure)
4. [Setup](#setup)
5. [Environment Variables](#environment-variables)
6. [Run the Server](#run-the-server)
7. [Run the Tests](#run-the-tests)
8. [API Usage](#api-usage)
9. [Screenshots](#screenshots)
10. [How Error Handling Works](#how-error-handling-works)
11. [Known Limitations](#known-limitations)
12. [Security](#security)

---

## Features

- One endpoint: `POST /posting`
- Input validation:
  - Message is not empty
  - Message is at most 200 characters
  - Exactly one link (CTA) in the message
  - The link must be a valid URL
- Platforms are chosen inside the app (the user does not pick them)
- All platforms run at the same time using `asyncio.gather`
- One failing platform never stops the others
- Credentials are read from environment variables (`.env`)

---

## Platforms Used

| #   | Platform        | What is posted                          | Official API docs                                                          |
| --- | --------------- | --------------------------------------- | -------------------------------------------------------------------------- |
| 1   | Facebook (Page) | Text post on a Page feed                | https://developers.facebook.com/docs/pages-api/posts                       |
| 2   | Instagram       | Image post with the message as caption  | https://developers.facebook.com/docs/instagram-platform/content-publishing |
| 3   | Threads         | Text post                               | https://developers.facebook.com/docs/threads/posting                       |
| 4   | Dev.to          | Published article (message is the body) | https://developers.forem.com/api/v1                                        |
| 5   | Bluesky         | Text post with a clickable link         | https://docs.bsky.app/docs/api/com-atproto-repo-create-record              |

---

## Project Structure

```text
automated-posting/
├── app/
│   ├── main.py                  # FastAPI app and the /posting endpoint
│   ├── schemas.py               # Request/response models and validation
│   ├── config.py                # Reads credentials from .env
│   ├── platforms/
│   │   ├── base.py              # Base class, error handling, result builder
│   │   ├── facebook.py
│   │   ├── instagram.py
│   │   ├── threads.py
│   │   ├── devto.py
│   │   └── bluesky.py
│   └── services/
│       └── posting_service.py   # Runs all platforms and collects results
├── assets/
│   └── insta_image.jpg          # Example Instagram image asset
├── tests/
│   └── test_posting.py          # Validation tests
├── screenshots/                 # Proof images used in this README
├── .env.example                 # Example environment file (fake values)
├── .gitignore
├── pytest.ini
├── requirements.txt
├── start.bat                    # Windows setup and server launcher
└── README.md
```

**How it works:** each platform has a `post()` method. The service runs them together, and the shared `publish()` method captures each platform's error independently so one failure does not stop the others.

---

## Setup

**Requirements:** Python 3.10 or newer.

### 1. Clone the repository

```bash
git clone https://github.com/MAliSheikh/Practical-Test.git
cd Practical-Test/automated-posting
```

### 2. Create your `.env` file

Windows:

```bash
copy .env.example .env
```

Mac / Linux:

```bash
cp .env.example .env
```

Edit `.env` and replace the example credentials with your own values. Do not commit this file.

### 3. Prepare the Python environment

On Windows, `start.bat` creates the virtual environment if needed and installs dependencies if missing.

On Mac / Linux, create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Environment Variables

| Variable                | Used by             | Description                                      |
| ----------------------- | ------------------- | ------------------------------------------------ |
| `FB_GRAPH_API_URL`      | Facebook, Instagram | Meta Graph API base URL                          |
| `FB_PAGE_ID`            | Facebook            | ID of your Facebook Page                         |
| `FB_PAGE_ACCESS_TOKEN`  | Facebook, Instagram | **Page** access token (not the user token)       |
| `IG_USER_ID`            | Instagram           | Instagram Business account ID linked to the Page |
| `IG_IMAGE_URL`          | Instagram           | Public direct link to a JPG image                |
| `THREADS_GRAPH_API_URL` | Threads             | Threads Graph API base URL                       |
| `THREADS_ACCESS_TOKEN`  | Threads             | Long-lived Threads access token                  |
| `DEVTO_API_URL`         | Dev.to              | Articles API endpoint                            |
| `DEVTO_API_KEY`         | Dev.to              | API key from Dev.to settings                     |
| `BLUESKY_API_URL`       | Bluesky             | Bluesky XRPC API base URL                        |
| `BLUESKY_HANDLE`        | Bluesky             | Your handle, e.g. `name.bsky.social`             |
| `BLUESKY_APP_PASSWORD`  | Bluesky             | App password (not your normal password)          |

Example `.env.example`:

```env
FB_GRAPH_API_URL=https://graph.facebook.com/v21.0
FB_PAGE_ID=your_page_id
FB_PAGE_ACCESS_TOKEN=your_page_access_token
IG_USER_ID=your_instagram_business_account_id
IG_IMAGE_URL=https://example.com/image.jpg
THREADS_GRAPH_API_URL=https://graph.threads.net/v1.0
THREADS_ACCESS_TOKEN=your_long_lived_threads_token
DEVTO_API_URL=https://dev.to/api/articles
DEVTO_API_KEY=your_devto_api_key
BLUESKY_API_URL=https://bsky.social/xrpc
BLUESKY_HANDLE=yourname.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

---

## Run the Server

On Windows:

```bat
start.bat
```

Or, after installing dependencies and activating the virtual environment:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Open the interactive API docs (Swagger):

http://localhost:4000/docs

---

## Run the Tests

Windows:

```bat
venv\Scripts\python.exe -m pytest -v
```

Mac / Linux (with the virtual environment activated):

```bash
python -m pytest -v
```

The tests check the input validation (too long, no link, two links, invalid URL). They do not post anything.

---

## API Usage

### Endpoint

```http
POST http://localhost:4000/posting
```

### Request body

```json
{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
```

### Sample curl request

```bash
curl -X POST http://localhost:4000/posting \
  -H "Content-Type: application/json" \
  -d '{"message": "Check out our latest business platform and grow your online visibility. https://example.com"}'
```

PowerShell:

```powershell
$body = @{ message = "Check out our latest business platform and grow your online visibility. https://example.com" } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://localhost:4000/posting" -Method Post -ContentType "application/json" -Body $body
```

### Sample success response

```json
{
  "success": true,
  "results": [
    {
      "platform": "Facebook",
      "status": "success",
      "posted_url": "https://www.facebook.com/1386503831217827_122094148131559967",
      "public_access": true,
      "date": "2026-11-16",
      "time": "12:14:17",
      "error": null
    },
    {
      "platform": "Instagram",
      "status": "success",
      "posted_url": "https://www.instagram.com/p/Dfyy2VIkbwm/",
      "public_access": true,
      "date": "2026-11-16",
      "time": "12:14:24",
      "error": null
    },
    {
      "platform": "Threads",
      "status": "success",
      "posted_url": "https://www.threads.com/@ai_ka_aloo/post/Dfyy2NZCAmQ",
      "public_access": true,
      "date": "2026-11-16",
      "time": "12:14:27",
      "error": null
    },
    {
      "platform": "Dev.to",
      "status": "success",
      "posted_url": "https://dev.to/malisheikh123/update-2026-11-16-121412-23nk",
      "public_access": true,
      "date": "2026-11-16",
      "time": "12:14:15",
      "error": null
    },
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/work97464.bsky.social/post/3n2fy5bszsd27",
      "public_access": true,
      "date": "2026-11-16",
      "time": "12:14:15",
      "error": null
    }
  ]
}
```

### Sample partial failure response

When one platform fails (here Dev.to has a wrong API key), the others still succeed:

```json
{
  "success": true,
  "results": [
    {
      "platform": "Dev.to",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "HTTP 401: {\"error\":\"unauthorized\",\"status\":401}"
    }
  ]
}
```

(Other platforms are not shown here to keep the example short. See screenshot 12.)

### Sample validation error (HTTP 422)

Request:

```json
{ "message": "Hello world, this message has no link" }
```

Response:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "message"],
      "msg": "Value error, Message must contain exactly one CTA link",
      "input": "Hello world, this message has no link"
    }
  ]
}
```

### Validation rules

| Input                              | Result |
| ---------------------------------- | ------ |
| No link                            | 422    |
| Two or more links                  | 422    |
| Invalid URL (e.g. `https://nodot`) | 422    |
| More than 200 characters           | 422    |
| Empty message                      | 422    |

---

## Screenshots

### 1. Swagger docs page

`http://localhost:4000/docs` showing the `POST /posting` endpoint.

![Docs page 1](screenshots/01.1-docs-page.png)
![Docs page 2](screenshots/01.2-docs-page.png)
![Docs page 3](screenshots/01.3-docs-page.png)

### 2. Validation errors (nothing is posted)

**No link**

![Error no link](screenshots/02-error-no-link.png)

**Two links**

![Error two links](screenshots/03-error-two-links.png.png)

**Invalid URL**

![Error invalid URL](screenshots/04-error-invalid-url.png)

**Message too long**

![Error too long](screenshots/05-error-too-long.png)

### 3. Successful response (all 5 platforms)

The full response is split into four screenshots.

![Success response part 1](screenshots/06.1-success-response.png)
![Success response part 2](screenshots/06.2-success-response.png)
![Success response part 3](screenshots/06.3-success-response.png)
![Success response part 4](screenshots/06.4-success-response.png)

### 4. Live posts

**Facebook**

![Facebook post](screenshots/07-facebook.png)

**Instagram**

![Instagram post](screenshots/08-instagram.png)

**Threads**

![Threads post](screenshots/09-threads.png)

**Dev.to**

![Dev.to post](screenshots/10-devto.png)

**Bluesky**

![Bluesky post](screenshots/11-bluesky.png)

### 5. Failure test (error isolation)

Dev.to was given a wrong API key on purpose. Dev.to shows `failed`, and the other platforms still succeed.

![Failure test](screenshots/12-failure-test.png)

---

## How Error Handling Works

- Each platform class has a `publish()` method in `base.py`.
- `publish()` wraps `post()` in a `try / except`.
- On success it returns `status: "success"` with the URL, date and time.
- On failure it returns `status: "failed"` with the error message.
- The service uses `asyncio.gather`, so all platforms run together and one failure does not affect the others.
- Missing required settings are detected early and reported as `Missing configuration in .env: ...`.
- The top-level `success` field is `true` when at least one platform succeeded.

---

## Known Limitations

- **Instagram needs an image.** Instagram does not allow text-only posts through the API. The app posts the image from `IG_IMAGE_URL` and uses the message as the caption.
- **Instagram media processing is asynchronous.** The app waits before publishing and retries when Instagram reports that the media container is not ready yet.
- **Facebook visibility.** While the Meta app is in Development mode, Facebook posts may not be visible to people who are logged out or have no role on the app. Switching the app to Live mode fixes this.
- **`public_access` is set to `true` after a successful post.** It is not checked by opening the URL without login.
- **Threads** needs a few seconds between creating and publishing a post, so the app waits briefly. Threads tokens also expire after about 60 days.
- **Dev.to** requires a title, so the app generates one from the current date and time.
- Facebook may block identical text posted many times in a short period.

---

## Security

- No API keys, tokens or passwords are stored in this repository.
- Real credentials live only in the local `.env` file, which is listed in `.gitignore`.
- Only `.env.example` (with fake values) is committed.
