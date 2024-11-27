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
        return  # Возврат в главное меню

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
        

        
        
        

        