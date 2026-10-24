# SlothGuard 🦥

A gentle, local ambient agent that watches for when you're stuck and offers calm, helpful tips.

## What it does

1. **Captures** your screen every 15-20 seconds (low resolution)
2. **Detects stagnation** - When the screen has stayed almost the same for ~90 seconds (SSIM comparison)
3. **Generates a tip** - Calls a local open-weight model via Ollama to create a short, calm tip
4. **Speaks it** - Uses Piper TTS to speak the tip aloud
5. **Cools down** - Goes silent for 5-8 minutes before monitoring again

Everything runs locally with open-source models. Your screen never leaves your machine.

## Why local/open-source?

A closed API version would have required sending screenshots of messy code and error messages to a third party. Running an open-weight model locally means the automation stays private, works offline, and costs nothing after setup. Plus, it rewards "laziness" - it only intervenes when you're actually stuck.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) with a vision model (recommended: `moondream`) or text model
- [Piper TTS](https://github.com/rhasspy/piper) (optional, will print if not installed)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Pull a model with Ollama:
```bash
ollama pull moondream  # Recommended - vision capable, lightweight
# or
ollama pull gemma2:2b
```

3. Download Piper voice model (optional):
   - Download `en_US-lessac-medium.onnx` and `en_US-lessac-medium.onnx.json` from [Piper voices](https://huggingface.co/rhasspy/piper-voices)
   - Place them in the `slothguard/` directory

## Usage

```bash
cd slothguard
python main.py
```

Press `Ctrl+C` to stop.

## Configuration

Edit `config.yaml` to tune:
- `capture.interval_seconds`: How often to check (15-20)
- `stagnation.threshold_seconds`: Time before considering stuck (90)
- `stagnation.ssim_threshold`: Similarity threshold (0.98 = almost identical)
- `ollama.model`: Which model to use
- `cooldown`: Min/max cooldown in minutes (5-8)

## Out of scope (intentionally omitted)

- Webcam / posture detection
- OCR / UI-loop detection
- System tray icon
- Fancy configuration UI
- Multiple sophisticated detectors

This is a complete, working ambient agent as specified.
