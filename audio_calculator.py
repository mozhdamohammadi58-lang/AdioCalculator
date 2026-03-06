# 📌 کتابخانه‌های مورد نیاز
import sounddevice as sd
import wavio
import speech_recognition as sr
import re

# -----------------------------------------------
# تبدیل اعداد فارسی یونیکد به اعداد صحیح
def convert_persian_numbers(word):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    if all(c in persian_digits for c in word):
        return int("".join(str(persian_digits.index(c)) for c in word))
    return None

# -----------------------------------------------
# تابع ضبط صدا و تبدیل به متن
def get_voice_input(duration=15, fs=44100):
    """
    ضبط صدا از میکروفون و ذخیره به فایل wav
    duration: مدت زمان ضبط (ثانیه) - طولانی‌تر برای جملات بلند
    fs: نرخ نمونه‌برداری
    """
    print("انتخاب زبان برای تشخیص صدا:")
    print("1. فارسی")
    print("2. انگلیسی")
    choice = input("عدد را وارد کنید: ")

    if choice == "1":
        language = "fa-IR"
    else:
        language = "en-US"

    # ضبط صدا
    print(f"🎤 لطفا صحبت کنید... (تا {duration} ثانیه)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write("voice.wav", recording, fs, sampwidth=2)

    # تبدیل صدا به متن
    r = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language=language)
        print(f"شما گفتید ({'فارسی' if language=='fa-IR' else 'انگلیسی'}):", text)
        return text
    except:
        print("متوجه نشدم 😢")
        return None

# -----------------------------------------------
# تابع تبدیل متن به اعداد و عملگرها
def parse_voice(text):
    if text is None:
        return []

    text = text.lower()

    # دیکشنری عملگرها
    operators = {
        "به علاوه": "+", "جمع": "+", "plus": "+",
        "منهای": "-", "منفی": "-", "minus": "-",
        "ضربدر": "*", "در": "*", "times": "*", "multiplied by": "*",
        "تقسیم بر": "/", "divided by": "/", "over": "/"
    }

    # دیکشنری اعداد انگلیسی و فارسی متنی
    numbers = {
        "صفر": 0, "یک": 1, "دو": 2, "سه": 3, "چهار": 4,
        "پنج": 5, "شش": 6, "هفت": 7, "هشت": 8, "نه": 9, "ده": 10,
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    # جایگزینی عبارات چندکلمه‌ای با عملگر
    for phrase, op in operators.items():
        text = text.replace(phrase, f" {op} ")

    words = text.split()
    tokens = []

    for word in words:
        # بررسی اعداد فارسی یونیکد
        num = convert_persian_numbers(word)
        if num is not None:
            tokens.append(num)
        elif word in numbers:
            tokens.append(numbers[word])
        elif word in operators.values():
            tokens.append(word)
        elif re.match(r'^\d+(\.\d+)?$', word):  # عدد انگلیسی یا اعشار
            tokens.append(float(word) if '.' in word else int(word))
        # بقیه نادیده گرفته می‌شوند

    return tokens

# -----------------------------------------------
# تابع محاسبه با الگوریتم شانتینگ یارد
def calculate_tokens(tokens):
    if not tokens:
        return "عبارت نامعتبر 😡"

    precedence = {'+':1, '-':1, '*':2, '/':2}
    output = []
    stack = []

    for token in tokens:
        if isinstance(token, (int, float)):
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            return "عبارت نامعتبر 😡"

    while stack:
        output.append(stack.pop())

    calc_stack = []
    for token in output:
        if isinstance(token, (int, float)):
            calc_stack.append(token)
        else:
            if len(calc_stack) < 2:
                return "عبارت نامعتبر 😡"
            b = calc_stack.pop()
            a = calc_stack.pop()
            if token == '+':
                calc_stack.append(a + b)
            elif token == '-':
                calc_stack.append(a - b)
            elif token == '*':
                calc_stack.append(a * b)
            elif token == '/':
                if b == 0:
                    return "تقسیم بر صفر ⚠️"
                calc_stack.append(a / b)

    if len(calc_stack) != 1:
        return "عبارت نامعتبر 😡"

    return calc_stack[0]

# -----------------------------------------------
# حلقه اصلی ماشین حساب
while True:
    choice = input("عملگر (+ - * /) یا 'v' برای صوت و 'q' برای خروج: ").strip()

    if choice.lower() == "q":
        break

    if choice.lower() == "v":
        voice_text = get_voice_input(duration=15)  # ضبط طولانی‌تر
        tokens = parse_voice(voice_text)
        result = calculate_tokens(tokens)
        print("نتیجه:", result)
        print("_" * 10)
        continue

    if choice not in ["+", "-", "*", "/"]:
        print("عملگر نامعتبر 😒")
        continue

    # حالت ورود دستی اعداد
    try:
        num1 = float(input("عدد اول: ").strip())
        num2 = float(input("عدد دوم: ").strip())
    except ValueError:
        print("ورودی نامعتبر 😡")
        continue

    tokens = [num1, choice, num2]
    result = calculate_tokens(tokens)
    print("نتیجه:", result)
    print("_" * 10)