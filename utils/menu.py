class Menu:
    @staticmethod
    def print_main():
        print("\n" + "=" * 50)
        print("АРМ СНАБЖЕНЦА - ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        print("1. Работа с поставщиками")
        print("2. Работа с материалами")
        print("3. Работа с закупками")
        print("4. Работа с планами закупок")
        print("5. Работа со складом")
        print("6. Отчеты")
        print("0. Выход")
        print("-" * 50)
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_suppliers():
        print("\n--- ПОСТАВЩИКИ ---")
        print("1. Просмотр всех поставщиков")
        print("2. Добавить поставщика")
        print("3. Изменить поставщика")
        print("4. Удалить поставщика")
        print("5. Назад")
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_materials():
        print("\n--- МАТЕРИАЛЫ ---")
        print("1. Просмотр всех материалов")
        print("2. Добавить материал")
        print("3. Изменить материал")
        print("4. Удалить материал")
        print("5. Назад")
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_purchases():
        print("\n--- ЗАКУПКИ ---")
        print("1. Просмотр всех закупок")
        print("2. Добавить закупку")
        print("3. Просмотр деталей закупки")
        print("4. Назад")
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_plans():
        print("\n--- ПЛАНЫ ЗАКУПОК ---")
        print("1. Просмотр всех планов")
        print("2. Добавить план")
        print("3. Изменить статус плана")
        print("4. Назад")
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_stock():
        print("\n--- СКЛАД ---")
        print("1. Просмотр остатков")
        print("2. Просмотр норм запаса")
        print("3. Назад")
        return input("Выберите действие: ").strip()

    @staticmethod
    def print_reports():
        print("\n--- ОТЧЕТЫ ---")
        print("1. Статистика по материалам")
        print("2. Материалы ниже нормы")
        print("3. Поставщики с закупками")
        print("4. Полный анализ закупок")
        print("5. Назад")
        return input("Выберите отчет: ").strip()

    @staticmethod
    def get_input(prompt, required=False):
        value = input(prompt).strip()
        if required and not value:
            print("Поле обязательно для заполнения")
            return None
        return value if value else None

    @staticmethod
    def confirm(message):
        answer = input(f"{message} (да/нет): ").strip().lower()
        return answer in ('да', 'д', 'yes', 'y')

    @staticmethod
    def get_float_input(prompt):
        try:
            return float(input(prompt).strip())
        except ValueError:
            return None