# AdioCalculator
A voice-controlled calculator in Python supporting Persian and English.
# VoiceCalc 🎤🧮

VoiceCalc is a **voice-controlled calculator** in Python supporting **Persian and English**.  
It can handle multi-step arithmetic expressions with Persian/English numbers and operators.

---

## Features
- 🗣️ Multilingual voice input (Persian/English)  
- ➕➖✖️➗ Multi-step operations  
- 🔢 Persian text & Unicode digits (۰–۹), English numbers  
- ⏱️ Up to 15 seconds audio recording  
- ⚡ Simple setup with Python libraries: `sounddevice`, `wavio`, `SpeechRecognition`  

---

## Usage
1. Run `voice_calc.py`  
2. Press `v` for voice input, `q` to quit, or enter operator for manual calculation  
3. Select language and speak your expression  

---

## Examples
You said (Persian): پنج جمع ۲ ضربدر ۳
Result: 11

You said (English): seven minus 4 plus 2
Result: 5

You said (Persian): ۵ بعلاوه ۴ به علاوه ۳ ضربدر ۲ تقسیم ۶ ضربدر ۷ منهای ۸
Result: 9

---

## Development
- Adjust recording duration (`duration=15`)  
- Add more languages or improve recognition for complex phrases  

---

## License
MIT License – free to use, modify, and share  

---

## Contact
Developer: [Mozhda Mohammadi]  
