class Purchase:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = """
            SELECT z.ID_Закупки, z.Дата_закупки, p.Имя, z.Статус_оплаты, 
                   z.Общая_стоимость, z.Ответственный
            FROM Закупка z
            JOIN Поставщик p ON z.ID_Поставщика = p.ID_Поставщика
            ORDER BY z.Дата_закупки DESC
        """
        return self.db.execute_query(query)

    def add(self, supplier_id, date, status, responsible, items):
        query = """
            INSERT INTO Закупка (ID_Поставщика, Дата_закупки, Статус_оплаты, Ответственный)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Закупки
        """
        purchase_id = self.db.execute_insert(query, (supplier_id, date, status, responsible))

        for item in items:
            query_item = """
                INSERT INTO Детали_Закупки (ID_Закупки, ID_Материала, Количество, 
                                           Цена_за_единицу, Партия, Срок_годности)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_insert(query_item, (purchase_id, item[0], item[1], item[2], item[3], item[4]))

        return purchase_id

    def get_details(self, purchase_id):
        query = """
            SELECT m.Наименование, dz.Количество, dz.Цена_за_единицу, 
                   dz.Общая_стоимость, dz.Партия
            FROM Детали_Закупки dz
            JOIN Материал m ON dz.ID_Материала = m.ID_Материала
            WHERE dz.ID_Закупки = %s
        """
        return self.db.execute_query(query, (purchase_id,))

    def display_table(self, purchases):
        if not purchases:
            print("\nСписок закупок пуст")
            return

        print("\n" + "=" * 95)
        print(f"{'ID':<5} {'Дата':<12} {'Поставщик':<25} {'Статус':<15} {'Сумма':<12} {'Ответственный':<15}")
        print("-" * 95)
        for p in purchases:
            print(f"{p[0]:<5} {str(p[1]):<12} {p[2][:23]:<25} {p[3]:<15} {p[4] or 0:<12} {p[5] or 'Н/Д':<15}")
        print("=" * 95)