# Overview
Using models from `Hugging Face`, with the interactive API, get insights about a given url.

# Setup

We recommend creating a new environment.

Install dependencies and the library in dev model:
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

# Usage

CLI:
```bash
conv_agent --help
```

The flag `-I` allows to run the code in an interactive mode. For a single prompt, you might want to use `--prompt`.

# Example:

To ask questions, in an interactive mode, about Apple from its wikipedia page, with additional content from the official Apple website
```bash
conv_agent --url "https://en.wikipedia.org/wiki/Apple_Inc." --content "You can also take a look at: https://www.apple.com/" -I
```

To ask a single question:
```bash
conv_agent --url "https://en.wikipedia.org/wiki/Apple_Inc." --content "You can also take a look at: https://www.apple.com/" --prompt "When was the first iPhone introduced?"
```

Outputs:
```
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ The first iPhone was introduced by Apple Inc. on January 9, 2007, at the Macworld          │
│ Conference & Expo in San Francisco. It went on sale later that year on June 29, 2007. The  │
│ original iPhone was a revolutionary device that combined a mobile phone, a mobile internet │
│ device, and an iPod into one touchscreen device with a user-friendly interface and         │
│ multi-touch gestures. It set the stage for the modern smart                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

The default model is `mistralai/Mixtral-8x7B-Instruct-v0.1`. This can be changed using the flag `--model`.
