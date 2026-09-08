class Material:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = """
            SELECT m.ID_Материала, m.Наименование, m.Единица_товара, 
                   m.Срок_годности, m.Категория, n.Норма
            FROM Материал m
            LEFT JOIN Норма_Запаса n ON m.ID_Материала = n.ID_Материала
            ORDER BY m.Наименование
        """
        return self.db.execute_query(query)

    def get_by_id(self, material_id):
        query = "SELECT * FROM Материал WHERE ID_Материала = %s"
        result = self.db.execute_query(query, (material_id,))
        return result[0] if result else None

    def add(self, name, unit, shelf_life, category):
        query = """
            INSERT INTO Материал (Наименование, Единица_товара, Срок_годности, Категория)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Материала
        """
        return self.db.execute_insert(query, (name, unit, shelf_life, category))

    def update(self, material_id, name=None, unit=None, shelf_life=None, category=None):
        updates = []
        params = []

        if name:
            updates.append("Наименование = %s")
            params.append(name)
        if unit:
            updates.append("Единица_товара = %s")
            params.append(unit)
        if shelf_life is not None:
            updates.append("Срок_годности = %s")
            params.append(shelf_life)
        if category:
            updates.append("Категория = %s")
            params.append(category)

        if not updates:
            return 0

        params.append(material_id)
        query = f"UPDATE Материал SET {', '.join(updates)} WHERE ID_Материала = %s"
        return self.db.execute_update(query, params)

    def delete(self, material_id):
        query = "DELETE FROM Материал WHERE ID_Материала = %s"
        return self.db.execute_update(query, (material_id,))

    def display_table(self, materials):
        if not materials:
            print("\nСписок материалов пуст")
            return

        print("\n" + "=" * 90)
        print(f"{'ID':<5} {'Наименование':<25} {'Ед.изм':<8} {'Срок годн':<10} {'Категория':<15} {'Норма':<10}")
        print("-" * 90)
        for m in materials:
            print(f"{m[0]:<5} {m[1][:23]:<25} {m[2]:<8} {m[3] or 'Н/Д':<10} {m[4] or 'Н/Д':<15} {m[5] or 'Н/Д':<10}")
        print("=" * 90)