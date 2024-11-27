import csv
import datetime
import json
import os


def menu() -> None:
    begin_text = 'Добро пожаловать в Персональный помощник!\nВыберите действие:\n1. Управление заметками\n2. Управление задачами\n3. Управление контактами\n4. Управление финансовыми записями\n5. Калькулятор\n6. Выход'
    print(begin_text)
    choice = input("Введите номер действия: ")
    if choice == '1':
        manage_notes()
    elif choice == '2':
        manage_tasks()
    elif choice == '3':
        manage_contacts()
    elif choice == '4':
        manage_finances()
    elif choice == '5':
        calculator()
    elif choice == '6':
        print("Выход из приложения...")
    else:
        print("Некорректный ввод. Пожалуйста, попробуйте снова.")


def manage_notes():
    note = Note(0, 'init_title', 'init_content', 'init_timespamp')
    message = '1.Создание новой заметки.\n2.Просмотр списка заметок.\n3.Просмотр подробностей заметки.\n4.Редактирование заметки.\n5.Удаление заметки.\n6.Импорт и экспорт заметок в формате CSV.\n7.Вернуться в меню'
    print(message)
    choice = input("Введите номер действия: ")
    if choice == '1':
        title = input("Введите название заметки: ")
        content = input("Введите содержимое заметки: ")
        timestamp = input("Введите дату и время создания заметки в формате  ДД-ММ-ГГГГ ЧЧ:ММ:СС: ")
        if not os.path.exists('notes.json'):
            id =  0
        else:
            with open('notes.json', 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
                id = len(notes_data)
        
        note.create_note(title, content, timestamp)
    elif choice == '2':
        if note.notes:
            notes_info = note.view_notes()
            print(notes_info)
        else:
            if not os.path.exists('notes.json'):
                print("Нет заметок.")
            else:
                with open('notes.json', 'r', encoding='utf-8') as f:
                    notes_data = json.load(f)
                    print(notes_data)
                
            
    elif choice == '3':
        note_id = input("Введите ID заметки: ")
        note_info = note.view_note_details(note_id)
        print(note_info)
        
    elif choice == '4':
        id = input("Введите ID записи")
        for note_n in note.notes:
            if note_n.id == id:
                title = input("Введите новое название заметки: ")
                content = input("Введите новое содержимое заметки: ")
                timestamp = input("Введите новые дату и время создания заметки в формате  ДД-ММ-ГГГГ ЧЧ:ММ:СС: ")
                note.edit_note(id, title, content, timestamp)
            else:
                print("Нет заметки с таким ID.")
        
    elif choice == '5':
        id = input("Введите ID записи")
        flag = False
        for note_n in note.notes:
            if note_n.id == id:
                flag = True
                note.delete_note(note_id)
        if not flag:
            print("Нет заметки с таким ID.")

    elif choice == '6':
        msg = '\n1.Импорт\n2. Экспорт'
        print(msg)
        chc = input("Введите номер действия: ")
        if chc == '1':
            filename = input("Введите название csv файла")
            note.import_from_csv(filename)

        elif chc == '2':
            filename = input("Введите название csv файла для экспорта")
            note.export_to_csv(filename)
        
    elif choice == '7':
        print("Выход в главное меню")
        menu()
    else:
        print("Некорректный ввод. Пожалуйста, попробуйте снова.")


def manage_tasks():
    task_manager = Task(0, '', '')  # Создаем экземпляр для управления задачами
    task_manager.load_tasks()  # Загружаем существующие задачи

    message = '1. Добавление новой задачи.\n2. Просмотр списка задач с отображением статуса, приоритета и срока.\n3. Отметка задачи как выполненной.\n4. Редактирование задачи.\n5. Удаление задачи.\n6. Импорт и экспорт задач в формате CSV.\n7. Вернуться в меню'
    
    print(message)
    choice = input("Введите номер действия: ")

    if choice == '1':
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Введите приоритет задачи (Высокий/Средний/Низкий): ")
        due_date = input("Введите срок выполнения задачи в формате ДД-ММ-ГГГГ: ")
        
        task_manager.create_task(title, description, priority, due_date)

    elif choice == '2':
        tasks_info = task_manager.view_tasks()
        if tasks_info:
            for task in tasks_info:
                print(f"ID: {task[0]}, Заголовок: {task[1]}, Выполнено: {task[2]}, Приоритет: {task[3]}, Срок: {task[4]}")
        else:
            print("Нет задач.")

    elif choice == '3':
        task_id = int(input("Введите ID задачи: "))
        task_info = task_manager.view_note_details(task_id)
        if task_info:
            print(f"ID: {task_info['id']}, Заголовок: {task_info['title']}, Описание: {task_info['description']}, "
                  f"Выполнено: {task_info['done']}, Приоритет: {task_info['priority']}, Срок: {task_info['due_date']}")
        else:
            print("Нет задачи с таким ID.")

    elif choice == '4':
        task_id = int(input("Введите ID задачи для редактирования: "))
        for task in task_manager.tasks:
            if task.id == task_id:
                title = input("Введите новое название задачи (или оставьте пустым для сохранения): ")
                description = input("Введите новое описание задачи (или оставьте пустым для сохранения): ")
                priority = input("Введите новый приоритет задачи (или оставьте пустым для сохранения): ")
                due_date = input("Введите новый срок выполнения (или оставьте пустым для сохранения): ")
                task_manager.edit_task(task_id, title or None, description or None, priority or None, due_date or None)
                break
        else:
            print("Нет задачи с таким ID.")

    elif choice == '5':
        task_id = int(input("Введите ID задачи для удаления: "))
        task_manager.delete_task(task_id)

    elif choice == '6':
        msg = '\n1. Импорт\n2. Экспорт'
        print(msg)
        chc = input("Введите номер действия: ")
        
        if chc == '1':
            filename = input("Введите название CSV файла для импорта: ")
            task_manager.import_from_csv(filename)

        elif chc == '2':
            filename = input("Введите название CSV файла для экспорта: ")
            task_manager.export_to_csv(filename)

    elif choice == '7':
        print("Выход в главное меню")
        menu()

    else:
        print("Некорректный ввод. Пожалуйста, попробуйте снова.")


def manage_contacts():
    contact = Contact(0, '')
    contact.load_contacts()
    message = '1. Добавление нового контакта.\n2. Поиск контакта по имени или номеру телефона.\n3. Редактирование контакта.\n4. Удаление контакта.\n5. Импорт и экспорт контактов в формате CSV.\n6. Вернуться в меню'
    print(message)
    choice = input("Введите номер действия: ")

    if choice == '1':
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        
        if not os.path.exists('contacts.json'):
            contact_id = 1
        else:
            with open('contacts.json', 'r', encoding='utf-8') as f:
                contacts_data = json.load(f)
                contact_id = len(contacts_data) + 1
        
        contact.create_contact(name, phone, email)

    elif choice == '2':
        query = input("Введите имя или номер телефона для поиска: ")
        found_contacts = contact.search_contact(query)
        
        if found_contacts:
            print("Найденные контакты:")
            for c in found_contacts:
                print(f"ID: {c.id}, Имя: {c.name}, Телефон: {c.phone}, Email: {c.email}")
        else:
            print("Контакты не найдены.")

    elif choice == '3':
        contact_id = int(input("Введите ID контакта для редактирования: "))
        for c in contact.contacts:
            if c.id == contact_id:
                name = input("Введите новое имя (или оставьте пустым для сохранения): ")
                phone = input("Введите новый номер телефона (или оставьте пустым для сохранения): ")
                email = input("Введите новый адрес электронной почты (или оставьте пустым для сохранения): ")
                contact.edit_contact(contact_id, name or None, phone or None, email or None)
                break
        else:
            print("Нет контакта с таким ID.")

    elif choice == '4':
        contact_id = int(input("Введите ID контакта для удаления: "))
        contact.delete_contact(contact_id)

    elif choice == '5':
        msg = '\n1. Импорт\n2. Экспорт'
        print(msg)
        chc = input("Введите номер действия: ")
        
        if chc == '1':
            filename = input("Введите название CSV файла для импорта: ")
            contact.import_from_csv(filename)

        elif chc == '2':
            filename = input("Введите название CSV файла для экспорта: ")
            contact.export_to_csv(filename)

    elif choice == '6':
        print("Выход в главное меню")
        menu()

    else:
        print("Некорректный ввод. Пожалуйста, попробуйте снова.")
 

def manage_finances():
    finance_record = FinanceRecord(0, 0.0, '', '', '')
    message = '1. Добавление новой финансовой записи.\n2. Просмотр всех записей.\n3. Генерация отчётов о финансовой активности за определённый период.\n4. Импорт и экспорт финансовых записей в формате CSV.\n5. Вернуться в меню'
    print(message)
    choice = input("Введите номер действия: ")
    if choice == '1':
        amount = float(input("Введите сумму операции (положительное число для доходов, отрицательное для расходов): "))
        category = input("Введите категорию операции: ")
        date = input("Введите дату операции в формате ДД-ММ-ГГГГ: ")
        description = input("Введите описание операции: ")
        
        if not os.path.exists('finance.json'):
            record_id = 1
        else:
            with open('finance.json', 'r', encoding='utf-8') as f:
                records_data = json.load(f)
                record_id = len(records_data) + 1
        
        finance_record.create_record(record_id,     amount, category, date, description)

    elif choice == '2':
        date_filter = input("Введите дату для фильтрации (или оставьте пустым): ")
        category_filter = input("Введите категорию для фильтрации (или оставьте пустым): ")
        filtered_records = finance_record.filter_records(date_filter or None, category_filter or None)
        records_info = finance_record.view_records(filtered_records)
        if records_info:
            for rec in records_info:
                print(f"ID: {rec[0]}, Сумма: {rec[1]}, Категория: {rec[2]}, Дата: {rec[3]}, Описание: {rec[4]}")
        else:
            print("Нет финансовых записей.")

    elif choice == '3':
        start_date = input("Введите начальную дату в формате ДД-ММ-ГГГГ: ")
        end_date = input("Введите конечную дату в формате ДД-ММ-ГГГГ: ")
        
        report = finance_record.generate_report(start_date, end_date)
        print("Отчет за указанный период:")
        print(report)

    elif choice == '4':
        msg = '\n1. Импорт\n2. Экспорт'
        print(msg)
        chc = input("Введите номер действия: ")
        
        if chc == '1':
            filename = input("Введите название CSV файла для импорта: ")
            finance_record.import_from_csv(filename)

        elif chc == '2':
            filename = input("Введите название CSV файла для экспорта: ")
            finance_record.export_to_csv(filename)

    elif choice == '5':
        print("Выход в главное меню")
        menu()

    else:
        print("Некорректный ввод. Пожалуйста, попробуйте снова.")


class Note:
    def __init__(self, id:int, title:str, content:str, timestamp:str) -> None:
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.notes = []

    
    def create_note(self, title, content, timestamp) -> None:
        note_id = len(self.notes) + 1
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        with open('notes.json', 'w', encoding='utf-8') as f:
            json.dump([note.to_dict() for note in self.notes], f, ensure_ascii=False, indent=4)


    def view_notes(self) -> list:
        return [(note.id, note.title, note.timestamp) for note in self.notes]


    def view_note_details(self, note_id:int) -> dict:
         for note in self.notes:
            if note.id == note_id:
                details = {
                    'id': self.id,
                    'title': self.title,
                    'content': self.content,
                    'timestamp': self.timestamp
                }
                return details
    

    def edit_note(self, note_id:int, title:str, content:str, timestamp:str) -> None:
        for note in self.notes:
            if note.id == note_id:
                if title:
                    note.title = title
                if content:
                    note.content = content
                if not timestamp:
                    note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                else:
                    note.timestamp = timestamp
                with open('notes.json', 'w', encoding='utf-8') as f:
                    json.dump([note.to_dict() for note in self.notes], f, ensure_ascii=False, indent=4)
    

    def delete_note(self, note_id:int) -> None:
        for note in self.notes:
            if note.id == note_id:
                self.notes.remove(note)
                with open('notes.json', 'w', encoding='utf-8') as f:
                    json.dump([note.to_dict() for note in self.notes], f, ensure_ascii=False, indent=4)
                break

    
    def import_from_csv(self, filename='notes.csv') -> None:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.create_note(row['Title'], row['Content'])

    
    def export_to_csv(self, filename='notes.csv') -> None:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Content', 'Timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])



class Task:
    def __init__(self, id: int, title: str, description: str, done: bool = False, priority: str = "Низкий", due_date: str = None) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date
        self.tasks = []


    def create_task(self, title: str, description: str, priority: str, due_date: str) -> None:
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, False, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()


    def view_tasks(self) -> list:
        return [(task.id, task.title, task.done, task.priority, task.due_date) for task in self.tasks]


    def mark_task_done(self, task_id: int) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.done = True
                self.save_tasks()
                break


    def edit_task(self, task_id: int, title: str = None, description: str = None, priority: str = None, due_date: str = None) -> None:
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if description:
                    task.description = description
                if priority:
                    task.priority = priority
                if due_date:
                    task.due_date = due_date
                self.save_tasks()
                break


    def delete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                break


    def import_from_csv(self, filename='tasks.csv') -> None:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.create_task(row['Title'], row['Description'], row['Priority'], row['Due Date'])


    def export_to_csv(self, filename='tasks.csv') -> None:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Description', 'Done', 'Priority', 'Due Date'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])


    def save_tasks(self) -> None:
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=4)


    def load_tasks(self) -> None:
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        

class Contact:
    def __init__(self, id: int, name: str, phone: str = None, email: str = None) -> None:
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.contacts = []


    def create_contact(self, name: str, phone: str, email: str) -> None:
        contact_id = len(self.contacts) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()


    def search_contact(self, query: str) -> list:
        return [contact for contact in self.contacts if query.lower() in contact.name.lower() or (contact.phone and query in contact.phone)]


    def edit_contact(self, contact_id: int, name: str = None, phone: str = None, email: str = None) -> None:
        for contact in self.contacts:
            if contact.id == contact_id:
                if name is not None:
                    contact.name = name
                if phone is not None:
                    contact.phone = phone
                if email is not None:
                    contact.email = email
                self.save_contacts()
                break


    def delete_contact(self, contact_id: int) -> None:
        for contact in self.contacts:
            if contact.id == contact_id:
                self.contacts.remove(contact)
                self.save_contacts()
                break


    def import_from_csv(self, filename='contacts.csv') -> None:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.create_contact(row['Name'], row['Phone'], row['Email'])


    def export_to_csv(self, filename='contacts.csv') -> None:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])


    def save_contacts(self) -> None:
        with open('contacts.json', 'w', encoding='utf-8') as f:
            json.dump([contact.__dict__ for contact in self.contacts], f, ensure_ascii=False, indent=4)


    def load_contacts(self) -> None:
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r', encoding='utf-8') as f:
                contacts_data = json.load(f)
                self.contacts = [Contact(**contact) for contact in contacts_data]


class FinanceRecord:
    def __init__(self, id: int, amount: float, category: str, date: str, description: str) -> None:
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.records = []

    def create_record(self, amount: float, category: str, date: str, description: str) -> None:
        record_id = len(self.records) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()

    def view_records(self, records_list=None) -> list:
        if not records_list:
            return [(record.id, record.amount, record.category, record.date, record.description) for record in self.records]
        else:
            return [(record.id, record.amount, record.category, record.date, record.description) for record in records_list]

    def filter_records(self, date: str = None, category: str = None) -> list:
        filtered_records = self.records
        if date:
            filtered_records = [record for record in filtered_records if record.date == date]
        if category:
            filtered_records = [record for record in filtered_records if record.category.lower() == category.lower()]
        return filtered_records

    def generate_report(self, start_date: str, end_date: str) -> dict:
        report = {
            'total_income': 0.0,
            'total_expense': 0.0,
            'balance': 0.0,
            'income_by_category': {},
            'expense_by_category': {}
        }
        
        for record in self.records:
            if start_date <= record.date <= end_date:
                if record.amount > 0:
                    report['total_income'] += record.amount
                    report['income_by_category'][record.category] = report['income_by_category'].get(record.category, 0) + record.amount
                else:
                    report['total_expense'] += abs(record.amount)
                    report['expense_by_category'][record.category] = report['expense_by_category'].get(record.category, 0) + abs(record.amount)

        report['balance'] = report['total_income'] - report['total_expense']
        return report

    def import_from_csv(self, filename='finance.csv') -> None:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row['Amount'])
                category = row['Category']
                date = row['Date']
                description = row['Description']
                self.create_record(amount, category, date, description)

    def export_to_csv(self, filename='finance.csv') -> None:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in self.records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])

    def save_records(self) -> None:
        with open('finance.json', 'w', encoding='utf-8') as f:
            json.dump([record.__dict__ for record in self.records], f, ensure_ascii=False, indent=4)

    def load_records(self) -> None:
        if os.path.exists('finance.json'):
            with open('finance.json', 'r', encoding='utf-8') as f:
                records_data = json.load(f)
                self.records = [FinanceRecord(**record) for record in records_data]


class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        try:
            return a / b
        except ValueError:
            return "Ошибка. Деление на ноль"

    def calculate(self):
        while True:
            print("\nВыберите операцию:")
            print("1. Сложение")
            print("2. Вычитание")
            print("3. Умножение")
            print("4. Деление")
            print("5. Выход")

            choice = input("Введите номер действия: ")

            if choice == '5':
                print("Выход в главное меню")
                menu()
            
            if choice not in ['1', '2', '3', '4', '5']:
                print("Некорректный ввод. Пожалуйста, попробуйте снова.")
                continue

            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))

                if choice == '1':
                    result = self.add(num1, num2)
                    operation = "Сложение"
                elif choice == '2':
                    result = self.subtract(num1, num2)
                    operation = "Вычитание"
                elif choice == '3':
                    result = self.multiply(num1, num2)
                    operation = "Умножение"
                elif choice == '4':
                    result = self.divide(num1, num2)
                    operation = "Деление"

                print(f"Результат {operation}: {result}")

            except ValueError as e:
                print(f"Ошибка ввода: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        

        