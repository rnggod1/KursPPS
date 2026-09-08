class Plan:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = """
            SELECT pp.ID_Плана, m.Наименование, pp.Плановый_месяц, 
                   pp.Статус_плана, pp.Дата_создания
            FROM План_Закупки pp
            JOIN Материал m ON pp.ID_Материала = m.ID_Материала
            ORDER BY pp.Плановый_месяц, m.Наименование
        """
        return self.db.execute_query(query)

    def add(self, material_id, month, status):
        query = """
            INSERT INTO План_Закупки (ID_Материала, Плановый_месяц, Статус_плана)
            VALUES (%s, %s, %s)
            RETURNING ID_Плана
        """
        return self.db.execute_insert(query, (material_id, month, status))

    def update_status(self, plan_id, status):
        query = "UPDATE План_Закупки SET Статус_плана = %s WHERE ID_Плана = %s"
        return self.db.execute_update(query, (status, plan_id))

    def display_table(self, plans):
        if not plans:
            print("\nСписок планов пуст")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<5} {'Материал':<25} {'Месяц':<12} {'Статус':<12} {'Создан':<12}")
        print("-" * 70)
        for p in plans:
            print(f"{p[0]:<5} {p[1][:23]:<25} {str(p[2]):<12} {p[3]:<12} {str(p[4]):<12}")
        print("=" * 70)