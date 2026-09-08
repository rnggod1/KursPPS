class Supplier:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        query = "SELECT * FROM Поставщик ORDER BY Имя"
        return self.db.execute_query(query)

    def get_by_id(self, supplier_id):
        query = "SELECT * FROM Поставщик WHERE ID_Поставщика = %s"
        result = self.db.execute_query(query, (supplier_id,))
        return result[0] if result else None

    def add(self, name, address, email, contacts, status, bank_details):
        query = """
            INSERT INTO Поставщик (Имя, Адрес, Почта, Контакты, 
                                   Статус_сотрудничества, Банк_реквизиты)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING ID_Поставщика
        """
        return self.db.execute_insert(query, (name, address, email, contacts, status, bank_details))

    def update(self, supplier_id, name=None, address=None, email=None,
               contacts=None, status=None, bank_details=None):
        updates = []
        params = []

        if name:
            updates.append("Имя = %s")
            params.append(name)
        if address:
            updates.append("Адрес = %s")
            params.append(address)
        if email:
            updates.append("Почта = %s")
            params.append(email)
        if contacts:
            updates.append("Контакты = %s")
            params.append(contacts)
        if status:
            updates.append("Статус_сотрудничества = %s")
            params.append(status)
        if bank_details:
            updates.append("Банк_реквизиты = %s")
            params.append(bank_details)

        if not updates:
            return 0

        params.append(supplier_id)
        query = f"UPDATE Поставщик SET {', '.join(updates)} WHERE ID_Поставщика = %s"
        return self.db.execute_update(query, params)

    def delete(self, supplier_id):
        query = "DELETE FROM Поставщик WHERE ID_Поставщика = %s"
        return self.db.execute_update(query, (supplier_id,))

    def display_table(self, suppliers):
        if not suppliers:
            print("\nСписок поставщиков пуст")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<5} {'Имя':<25} {'Статус':<15} {'Контакты':<20}")
        print("-" * 80)
        for s in suppliers:
            print(f"{s[0]:<5} {s[1][:23]:<25} {s[5] or 'Н/Д':<15} {s[4] or 'Н/Д':<20}")
        print("=" * 80)