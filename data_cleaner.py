import json

# Имитируем "грязные" данные от заказчика (дубликаты, пробелы, разный регистр)
bad_data = [
    {"name": " иван иванов ", "phone": "+7 (999) 111-22-33", "amount": " 1500 руб "},
    {"name": "иван иванов", "phone": "79991112233", "amount": "1500"},
    {"name": "Мария С.", "phone": "89115554433", "amount": "3200 p."},
    {"name": " алексей ", "phone": "+79001234567", "amount": "abc"} # тут ошибка в сумме
]

def clean_data(data):
    print("🧹 Запуск скрипта очистки данных...")
    cleaned_records = []
    seen_phones = set()

    for item in data:
        # 1. Очищаем имя от лишних пробелов и делаем с заглавной буквы
        name = item["name"].strip().title()
        
        # 2. Приводим телефон к единому стандарту (только цифры)
        phone = "".join(filter(str.isdigit, item["phone"]))
        if phone.startswith("8"):
            phone = "7" + phone[1:]
        elif phone.startswith("9"):
            phone = "7" + phone

        # 3. Проверяем на дубликаты по номеру телефона
        if phone in seen_phones:
            print(f"⚠️ Удален дубликат для: {name} ({phone})")
            continue
        seen_phones.add(phone)

        # 4. Очищаем сумму и превращаем в число
        amount_raw = "".join(filter(str.isdigit, item["amount"]))
        amount = int(amount_raw) if amount_raw.isdigit() else 0

        cleaned_records.append({
            "Имя": name,
            "Телефон": f"+{phone}" if phone else "Нет номера",
            "Сумма_выручки": amount
        })

    # Сохраняем результат в красивый файл JSON
    with open("clean_report.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_records, f, ensure_ascii=False, indent=4)
    
    print("\n✅ Очистка завершена! Результат сохранен в 'clean_report.json'")

if __name__ == "__main__":
    clean_data(bad_data)
