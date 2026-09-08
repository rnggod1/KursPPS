from database import Database
from models.supplier import Supplier
from models.material import Material
from models.purchase import Purchase
from models.plan import Plan
from models.stock import Stock
from reports.report_manager import ReportManager
from utils.menu import Menu

DB_CONFIG = {
    "dbname": "KursPPS",
    "user": "postgres",
    "password": "1",
    "host": "localhost",
    "port": "5432"
}


class Application:
    def __init__(self):
        self.db = None
        self.supplier_model = None
        self.material_model = None
        self.purchase_model = None
        self.plan_model = None
        self.stock_model = None
        self.report_manager = None
        self.menu = Menu()

    def initialize(self):
        self.db = Database(**DB_CONFIG)
        if not self.db.connect():
            print("Не удалось подключиться к БД")
            return False

        self.supplier_model = Supplier(self.db)
        self.material_model = Material(self.db)
        self.purchase_model = Purchase(self.db)
        self.plan_model = Plan(self.db)
        self.stock_model = Stock(self.db)
        self.report_manager = ReportManager(self.db)

        print("Подключение к БД успешно установлено")
        return True

    def shutdown(self):
        if self.db:
            self.db.disconnect()
            print("Соединение с БД закрыто")

    def run(self):
        if not self.initialize():
            return

        try:
            while True:
                choice = self.menu.print_main()

                if choice == '0':
                    print("\nВыход из приложения")
                    break
                elif choice == '1':
                    self.suppliers_workflow()
                elif choice == '2':
                    self.materials_workflow()
                elif choice == '3':
                    self.purchases_workflow()
                elif choice == '4':
                    self.plans_workflow()
                elif choice == '5':
                    self.stock_workflow()
                elif choice == '6':
                    self.reports_workflow()
                else:
                    print("\nНеверный выбор")

                input("\nНажмите Enter для продолжения...")

        except KeyboardInterrupt:
            print("\nПрограмма прервана")
        except Exception as e:
            print(f"\nОшибка: {e}")
        finally:
            self.shutdown()

    def suppliers_workflow(self):
        while True:
            choice = self.menu.print_suppliers()

            if choice == '1':
                suppliers = self.supplier_model.get_all()
                self.supplier_model.display_table(suppliers)
            elif choice == '2':
                self.add_supplier()
            elif choice == '3':
                self.update_supplier()
            elif choice == '4':
                self.delete_supplier()
            elif choice == '5':
                break

    def add_supplier(self):
        print("\n--- ДОБАВЛЕНИЕ ПОСТАВЩИКА ---")
        name = self.menu.get_input("Имя: ", required=True)
        if not name: return

        address = self.menu.get_input("Адрес: ")
        email = self.menu.get_input("Почта: ")
        contacts = self.menu.get_input("Контакты: ")
        status = self.menu.get_input("Статус (Активен/Приостановлен/Завершен): ") or "Активен"
        bank = self.menu.get_input("Банковские реквизиты: ")

        try:
            supplier_id = self.supplier_model.add(name, address, email, contacts, status, bank)
            print(f"Поставщик добавлен с ID: {supplier_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update_supplier(self):
        suppliers = self.supplier_model.get_all()
        self.supplier_model.display_table(suppliers)

        try:
            supplier_id = int(self.menu.get_input("ID поставщика: "))
        except ValueError:
            return

        supplier = self.supplier_model.get_by_id(supplier_id)
        if not supplier:
            print("Поставщик не найден")
            return

        print("\n(Оставьте поле пустым, чтобы не менять)")
        name = self.menu.get_input("Новое имя: ")
        address = self.menu.get_input("Новый адрес: ")
        email = self.menu.get_input("Новая почта: ")
        contacts = self.menu.get_input("Новые контакты: ")
        status = self.menu.get_input("Новый статус: ")
        bank = self.menu.get_input("Новые реквизиты: ")

        try:
            self.supplier_model.update(supplier_id, name, address, email, contacts, status, bank)
            print("Данные поставщика обновлены")
        except Exception as e:
            print(f"Ошибка: {e}")

    def delete_supplier(self):
        suppliers = self.supplier_model.get_all()
        self.supplier_model.display_table(suppliers)

        try:
            supplier_id = int(self.menu.get_input("ID поставщика для удаления: "))
        except ValueError:
            return

        if self.menu.confirm("Вы уверены?"):
            try:
                self.supplier_model.delete(supplier_id)
                print("Поставщик удален")
            except Exception as e:
                print(f"Ошибка: {e}")

    def materials_workflow(self):
        while True:
            choice = self.menu.print_materials()

            if choice == '1':
                materials = self.material_model.get_all()
                self.material_model.display_table(materials)
            elif choice == '2':
                self.add_material()
            elif choice == '3':
                self.update_material()
            elif choice == '4':
                self.delete_material()
            elif choice == '5':
                break

    def add_material(self):
        print("\n--- ДОБАВЛЕНИЕ МАТЕРИАЛА ---")
        name = self.menu.get_input("Наименование: ", required=True)
        if not name: return
        unit = self.menu.get_input("Единица измерения: ", required=True)
        if not unit: return
        shelf_life = self.menu.get_input("Срок годности (дней): ")
        category = self.menu.get_input("Категория: ")

        try:
            material_id = self.material_model.add(name, unit, int(shelf_life) if shelf_life else None, category)
            print(f"Материал добавлен с ID: {material_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update_material(self):
        materials = self.material_model.get_all()
        self.material_model.display_table(materials)

        try:
            material_id = int(self.menu.get_input("ID материала: "))
        except ValueError:
            return

        material = self.material_model.get_by_id(material_id)
        if not material:
            print("Материал не найден")
            return

        print("\n(Оставьте поле пустым, чтобы не менять)")
        name = self.menu.get_input("Новое наименование: ")
        unit = self.menu.get_input("Новая единица измерения: ")
        shelf_life = self.menu.get_input("Новый срок годности: ")
        category = self.menu.get_input("Новая категория: ")

        try:
            self.material_model.update(material_id, name, unit,
                                       int(shelf_life) if shelf_life else None, category)
            print("Данные материала обновлены")
        except Exception as e:
            print(f"Ошибка: {e}")

    def delete_material(self):
        materials = self.material_model.get_all()
        self.material_model.display_table(materials)

        try:
            material_id = int(self.menu.get_input("ID материала для удаления: "))
        except ValueError:
            return

        if self.menu.confirm("Вы уверены?"):
            try:
                self.material_model.delete(material_id)
                print("Материал удален")
            except Exception as e:
                print(f"Ошибка: {e}")

    def purchases_workflow(self):
        while True:
            choice = self.menu.print_purchases()

            if choice == '1':
                purchases = self.purchase_model.get_all()
                self.purchase_model.display_table(purchases)
            elif choice == '2':
                self.add_purchase()
            elif choice == '3':
                self.show_purchase_details()
            elif choice == '4':
                break

    def add_purchase(self):
        print("\n--- ДОБАВЛЕНИЕ ЗАКУПКИ ---")

        suppliers = self.supplier_model.get_all()
        self.supplier_model.display_table(suppliers)

        try:
            supplier_id = int(self.menu.get_input("ID поставщика: "))
        except ValueError:
            return

        date = self.menu.get_input("Дата закупки (ГГГГ-ММ-ДД): ", required=True)
        if not date: return
        status = self.menu.get_input("Статус оплаты: ") or "Не оплачено"
        responsible = self.menu.get_input("Ответственный: ")

        items = []
        materials = self.material_model.get_all()
        self.material_model.display_table(materials)

        print("\nДобавление позиций (пустой ID для завершения):")
        while True:
            try:
                material_id_input = self.menu.get_input("ID материала: ")
                if not material_id_input:
                    break
                material_id = int(material_id_input)
                quantity = float(self.menu.get_input("Количество: "))
                price = float(self.menu.get_input("Цена за единицу: "))
                lot = self.menu.get_input("Партия: ")
                expiry = self.menu.get_input("Срок годности (ГГГГ-ММ-ДД): ")

                items.append((material_id, quantity, price, lot, expiry))
            except ValueError:
                print("Некорректные данные, попробуйте снова")

        if not items:
            print("Нет позиций для добавления")
            return

        try:
            purchase_id = self.purchase_model.add(supplier_id, date, status, responsible, items)
            print(f"Закупка добавлена с ID: {purchase_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def show_purchase_details(self):
        try:
            purchase_id = int(self.menu.get_input("ID закупки: "))
        except ValueError:
            return

        details = self.purchase_model.get_details(purchase_id)
        if details:
            print("\n" + "=" * 70)
            print(f"ДЕТАЛИ ЗАКУПКИ №{purchase_id}")
            print("=" * 70)
            for d in details:
                print(f"  {d[0]}: {d[1]} x {d[2]} = {d[3]} | Партия: {d[4]}")
            print("=" * 70)
        else:
            print("Детали не найдены")

    def plans_workflow(self):
        while True:
            choice = self.menu.print_plans()

            if choice == '1':
                plans = self.plan_model.get_all()
                self.plan_model.display_table(plans)
            elif choice == '2':
                self.add_plan()
            elif choice == '3':
                self.update_plan_status()
            elif choice == '4':
                break

    def add_plan(self):
        print("\n--- ДОБАВЛЕНИЕ ПЛАНА ---")

        materials = self.material_model.get_all()
        self.material_model.display_table(materials)

        try:
            material_id = int(self.menu.get_input("ID материала: "))
        except ValueError:
            return

        month = self.menu.get_input("Плановый месяц (ГГГГ-ММ-01): ", required=True)
        if not month: return
        status = self.menu.get_input("Статус: ") or "Проект"

        try:
            plan_id = self.plan_model.add(material_id, month, status)
            print(f"План добавлен с ID: {plan_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update_plan_status(self):
        plans = self.plan_model.get_all()
        self.plan_model.display_table(plans)

        try:
            plan_id = int(self.menu.get_input("ID плана: "))
        except ValueError:
            return

        status = self.menu.get_input("Новый статус (Проект/Утвержден/Выполнен/Отменен): ", required=True)
        if not status: return

        try:
            self.plan_model.update_status(plan_id, status)
            print("Статус плана обновлен")
        except Exception as e:
            print(f"Ошибка: {e}")

    def stock_workflow(self):
        while True:
            choice = self.menu.print_stock()

            if choice == '1':
                stocks = self.stock_model.get_all()
                self.stock_model.display_table(stocks)
            elif choice == '2':
                norms = self.stock_model.get_norms()
                print("\n" + "=" * 50)
                print("НОРМЫ ЗАПАСА")
                print("=" * 50)
                for n in norms:
                    print(f"  {n[0]}: {n[1]} (установлена {n[2]})")
                print("=" * 50)
            elif choice == '3':
                break

    def reports_workflow(self):
        while True:
            choice = self.menu.print_reports()

            if choice == '1':
                self.report_manager.materials_statistics()
            elif choice == '2':
                self.report_manager.materials_below_norm()
            elif choice == '3':
                self.report_manager.suppliers_with_purchases()
            elif choice == '4':
                self.report_manager.full_analysis()
            elif choice == '5':
                break


def main():
    Application().run()


if __name__ == "__main__":
    main()