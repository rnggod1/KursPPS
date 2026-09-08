class Stock:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = """
            SELECT s.ID_Запись, m.Наименование, s.Количество, s.Дата_поставки,
                   sec.Наименование, s.Статус_партии
            FROM Склад s
            JOIN Материал m ON s.ID_Материала = m.ID_Материала
            LEFT JOIN Сектор_Склада sec ON s.ID_Сектора = sec.ID_Сектора
            ORDER BY m.Наименование, s.Дата_поставки DESC
        """
        return self.db.execute_query(query)

    def get_norms(self):
        query = """
            SELECT m.Наименование, n.Норма, n.Дата_установки
            FROM Норма_Запаса n
            JOIN Материал m ON n.ID_Материала = m.ID_Материала
            ORDER BY m.Наименование
        """
        return self.db.execute_query(query)

    def display_table(self, stocks):
        if not stocks:
            print("\nСклад пуст")
            return

        print("\n" + "=" * 85)
        print(f"{'ID':<5} {'Материал':<25} {'Кол-во':<10} {'Дата пост':<12} {'Сектор':<10} {'Статус':<15}")
        print("-" * 85)
        for s in stocks:
            print(f"{s[0]:<5} {s[1][:23]:<25} {s[2]:<10} {str(s[3]):<12} {s[4] or 'Н/Д':<10} {s[5]:<15}")
        print("=" * 85)