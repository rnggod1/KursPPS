class ReportManager:
    def __init__(self, db):
        self.db = db

    def materials_statistics(self):
        print("\n" + "=" * 80)
        print("СТАТИСТИКА ПО МАТЕРИАЛАМ")
        print("=" * 80)

        query = "SELECT * FROM Статистика_Материалов"
        results = self.db.execute_query(query)

        for row in results:
            print(f"\nМатериал: {row[1]}")
            print(f"  Единица: {row[2]}")
            print(f"  Остаток: {row[3]}")
            print(f"  Норматив: {row[4]}")
            print(f"  Дефицит: {row[5]}")

    def materials_below_norm(self):
        print("\n" + "=" * 80)
        print("МАТЕРИАЛЫ НИЖЕ НОРМЫ")
        print("=" * 80)

        query = "SELECT * FROM Материалы_Ниже_Нормы"
        results = self.db.execute_query(query)

        if not results:
            print("Все материалы в норме")
            return

        for row in results:
            print(f"\nМатериал: {row[1]}")
            print(f"  Остаток: {row[2]}, Норма: {row[3]}, Дефицит: {row[4]}")

    def suppliers_with_purchases(self):
        print("\n" + "=" * 80)
        print("ПОСТАВЩИКИ С ЗАКУПКАМИ")
        print("=" * 80)

        query = "SELECT * FROM Поставщики_С_Закупками"
        results = self.db.execute_query(query)

        for row in results:
            print(f"\nПоставщик: {row[1]}")
            print(f"  Статус: {row[2]}")
            print(f"  Закупок: {row[3]}, Сумма: {row[4]}")
            print(f"  Последняя закупка: {row[5]}")

    def full_analysis(self):
        print("\n" + "=" * 80)
        print("ПОЛНЫЙ АНАЛИЗ ЗАКУПОК")
        print("=" * 80)

        query = "SELECT * FROM Полный_Анализ_Закупок LIMIT 10"
        results = self.db.execute_query(query)

        for row in results:
            print(f"\nЗакупка {row[0]} от {row[1]}")
            print(f"  Поставщик: {row[2]}")
            print(f"  Материал: {row[3]}")
            print(f"  Кол-во: {row[4]}, Цена: {row[5]}, Сумма: {row[6]}")