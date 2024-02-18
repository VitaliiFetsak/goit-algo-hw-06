from collections import UserDict
import re

# Class Field value
class Field:
    def __init__(self, value=''):
        self.value = value
        
    def setValue(self, value:str):
        self.value = value
    
    def getValue(self):
        return self.value
    
# Class for saving contact`s` name
class Name(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Class for saving unitary number with assign to standart type    
class Phone(Field):
    def __init__(self, value:str):
        if len(value) == 10 and re.search(r'\d{10}', value):
            self.value = value
        else:
            self.value = None

    def setValue(self, value: str):
        if len(value) == 10 and re.search(r'\d{10}', value):
            self.value = value
        else:
            self.value = None

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def getName(self):
        return f'"{self.name.value}"'
    
    def getRecord(self):
        return f"Contact name: {self.name.value}, \
        Contact numbers: {'; '.join(p.value for p in self.phones)}"

    def find_phone(self, phone:Phone):
        i = -1
        for p in self.phones:
            i+=1
            if phone.value == p.value:  
                return (True, i)
            else:
                continue
        return (False, -1)
        
    def add_phone(self, phone:Phone): 
        if phone.value and not self.find_phone(phone)[0]:
            self.phones.append(phone)

    def remove_phone(self, phone:Phone):
        if self.find_phone(phone)[0]:
            self.phones.remove(phone)

    def edit_phone(self, value_old:str, value_new:str):
        phone_old = Phone(value_old)
        phone_new = Phone(value_new)
        is_phone_old, i = self.find_phone(phone_old)
        is_phone_new = self.find_phone(phone_new)[0]
        if not is_phone_new and is_phone_old:
            self.phones[i]=phone_new

class AddressBook(UserDict):
    def getBook(self):
        string = ''
        for k in self.data.items():
            string += f'{k[0].value:<15}\n\
        tel.: {"; ".join(p.value for p in k[1].phones)}\n'    
        return string
    
    def add_record(self, record:Record):
        key = record.name
        self.data[key]=record
    
    def find_record(self, name:str):
        for k in self.data.items():
            if k[0].value == name:
                return f'tel.: {"; ".join(p.value for p in k[1].phones)}'  
            else:
                continue
    
    def delete(self, name:str):
        del_rec = None
        for k in self.data.items():
            if k[0].value == name:
                del_rec = k[1]
                break  
            else:
                continue
        if del_rec:
            self.data.pop(del_rec.name)
        return 'Success' if del_rec else 'There is no record'

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find_record("John")
john_record.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john_record.find_phone("5555555555")
print(f"{john_record.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")