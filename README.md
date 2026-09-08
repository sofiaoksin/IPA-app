# 🦜 IPA Learning App

A Streamlit app for learning and practicing the International Phonetic Alphabet (IPA).

## ⛓️‍💥 Useful Links
[Wikimedia Commons' General Phonetics collection](https://commons.wikimedia.org/wiki/General_phonetics)

[Interactive IPA Chart](https://www.ipachart.com)

## 🧩 Quiz

### Modes:

- **Easy:** 5 questions with 3 answer options, ideal for beginners.
- **Medium:** 18 questions with 5 answer options, covering about half of the IPA symbols.
- **Hard:** 35 questions with 5 answer options, covering the full IPA symbol set.

## 🚀 Run locally

### Prerequisites

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)

### Setup

1. Clone the repository and open its folder:

	```bash
	git clone <repository-url>
	cd IPA-app
	```

2. Install the project dependencies:

	```bash
	uv sync
	```

3. Start the Streamlit app:

```bash
uv run streamlit run src/main.py
```

4. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 🤝 Audio credits

The audio clips are the work of Peter Isotalo and User:Denelson83. They are
available under a free and/or copyleft licence through [Wikimedia Commons'
General Phonetics collection](https://commons.wikimedia.org/wiki/General_phonetics).

## Future improvements

Just a few ideas

- Add more IPA symbols
- Targeted learning: Store learned symbols and unlearned symbols in different folders
- Add more learning modes
    - Memory
    - Connect