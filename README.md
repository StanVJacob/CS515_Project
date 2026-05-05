# CS515 Project

A real-time English → Simplified Chinese translator. Speak into your microphone and watch the translation appear live in your browser.

---

## Getting Started

These instructions will get the project running on your local machine for development and testing.

### Prerequisites

Make sure the following are installed before you begin:

| Requirement | Notes |
|---|---|
| **Python 3.9+** | [Download here](https://www.python.org/downloads/) |
| **Git** | [Download here](https://git-scm.com/downloads) |
| **Chrome or Edge** | Required — Firefox/Safari do not support the Web Speech API |

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/StanVJacob/CS515_Project.git
cd CS515_Project
```

#### 2. Create a virtual environment

A virtual environment keeps this project's dependencies isolated from your system Python.

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```


#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs two packages:

- **Flask** — minimal web server for the `/translate` endpoint
- **deep-translator** — wraps Google Translate's free public endpoint

#### 4. Run the application

```bash
python app.py
```

You should see output similar to:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
```

Open **http://127.0.0.1:5001** in Chrome or Edge, click **Start**, and grant microphone access when prompted.

> **macOS users:** Port `5001` is used to avoid a conflict with AirPlay Receiver, which occupies port `5000` by default. If `5001` is also taken, edit the last line of `app.py` to choose another port.

### Deactivating the environment

When you're done working, leave the virtual environment with:

```bash
deactivate
```

Re-activate it next time with `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\Activate.ps1` (Windows).

---

## Tech Stack Overview

**Goal:** Real time translation.

## Workflow

1. **Voice to text** (Front end)
2. **Text sent to backend**
3. **Backend translates** the received text into the targeted language

## Learning Outcomes Covered

### Organize data, code, and functionality by creating and extending object classes

The backend logic in `hw7.py` is organized into classes with clear
responsibilities:

- `LanguageManager` stores supported languages and validates language codes.
- `TranslationService` translates cleaned transcript text.
- `ChineseTranslationService` and `SpanishTranslationService` extend
  `TranslationService` for language-specific behavior.
- `SubtitleProcessor` coordinates language validation and translation.

The project also uses inheritance through `BaseTranslationService` and
`BaseSubtitleProcessor`, which define shared interfaces for the concrete
classes.

### Validate correct program behavior by writing unit tests

`test_hw7.py` contains unit tests for backend behavior, including:

- `translate_text()` returning expected translated output when given a known
  input.
- `validate_language()` accepting supported language codes and rejecting
  unsupported values.
- subtitle processing, input cleaning, and supported-language lookup.

The translation tests use a fake translator so they can run reliably without a
network call.

## Tools


### 1. Web Speech API (Free)
Used on the front end to convert voice into text.

Documentation: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

### 3. Deep Translator (Free, Open Source)
Used on the backend to translate the received text.

Documentation: https://deep-translator.readthedocs.io/en/latest/


