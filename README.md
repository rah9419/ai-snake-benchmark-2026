# 🐍 AI Coding Benchmark 2026 (Snake Game)

This repository contains the source code for the "Architect Test" conducted by **TestedByHuman.com**.

We asked 6 different AI models to write a complete Snake game in Python using Pygame.

## 📂 The Files

### ✅ The Winners (Work Perfectly)
* **`snake_gpt5.2_thinking.py`** - Best architecture (Class-based, WASD support).
* **`snake_gpt5.2_auto.py`** - Great for quick scripting.
* **`snake_gpt5.1_thinking.py`** - Works, but outdated logic.
* **`snake_o3.py`** - Minimalist, functional code.

### ❌ The Failures (Broken Logic)
For these models, we have provided both the **RAW** (broken) output and the **FIXED** version so you can see the bugs.

* **GPT-5.1 Instant** (`_RAW.py` vs `_FIXED.py`)
  * *Bug:* Grid misalignment (Snake passed through food).
* **GPT-5.2 Instant** (`_RAW.py` vs `_FIXED.py`)
  * *Bug:* Aggressive speed scaling (Game became unplayable).

## 🚀 How to Run
1. Install Pygame: `pip install pygame`
2. Run any file: `python snake_gpt5.2_thinking.py`

---
*Read the full review and benchmark at [TestedByHuman.com](https://testedbyhuman.com)*
