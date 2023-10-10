from collections import UserDict
from datetime import datetime, date
import json
import re

class PhoneTooShortError(ValueError):
    pass

class PhoneIncludesNotOnlyNumbersError(ValueError):
    pass


class Field:
    def __init__(self, value):
        self.value = value  

    def __str__(self):
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if len(new_value) != 10:
            raise  PhoneTooShortError("Phone number should be 10 digits long.")
        if not self.value.isdigit():
            raise PhoneIncludesNotOnlyNumbersError("Phone number should only include digits.")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        self._value = value
    
    @property
    def birthday(self):
        return self._value
    
    @birthday.setter
    def birthday(self, new_value) -> datetime:
        if new_value:
            self._value = date.fromisoformat(new_value)

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone_to_remove):
         search_for_phone = list(filter(lambda phone: phone.value == phone_to_remove, self.phones))
         if search_for_phone:
             self.phones.remove(search_for_phone[0])
         

    def edit_phone(self, old_phone, new_phone):
        search_for_phone = list(filter(lambda phone: phone.value == old_phone, self.phones))
        if search_for_phone:
            search_for_phone[0].value = new_phone
        else:
            raise ValueError
    
    def find_phone(self, phone_to_find):
        search_for_phone = list(filter(lambda phone: phone.value == phone_to_find, self.phones))
        if search_for_phone:
            return search_for_phone[0]
        
    def days_to_birthday(self):
        if self.birthday:
            return (self.birthday - datetime.today()).days
        return f"There is ot birthday input for {self.name}."
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    


    def find(self, pattern):
        pattern = pattern.strip()
        found_names = []
        for key, value in self.data.items():
            if re.search(pattern, key):
                found_names.append(key)
            phone_values = [phone._value if not value.phones else None for phone in value.phones ]
            for phone_value in phone_values:
                if phone_value:
                    if re.search(pattern, phone_value):
                        found_names.append(key)
        
        return found_names
       
    
    def delete(self, name):
        self.data.pop(name, 'Name not present')
    
    def iterator(self, number_of_pages = 2):
        return Iterable(number_of_pages, self.data)
    
    def save_book_json(self, name_of_book : str = 'address_book'):
        self._name_of_book = '.'.join([name_of_book, 'json'])
        with open(self._name_of_book, 'w') as fh:
            book_with_str_keys_and_proper_values = {}
            for key, value in self.data.items():
                book_with_str_keys_and_proper_values[key] = {
                    'phones' : [phone._value for phone in value.phones] if not value.phones else None,
                    'birthday' : value.birthday._value.strftime("%Y-%m-%d")
                }
            json.dump(book_with_str_keys_and_proper_values, fh)
    
    def load_book_json(self, name_of_book : str = 'address_book'):
        self._name_of_book = '.'.join([name_of_book, 'json'])
        with open(self._name_of_book, 'r') as fh:
            json_book_data = json.load(fh)
            for key, value in json_book_data.items():
                self.data[key] = Record(key, value['birthday'])
                if not value['phones']:
                    for phone in value['phones']:
                        self.data[key].add_phone(phone)
    

             

class Iterable:
    def __init__(self, number_to_display, sequence):
        self._end_point = number_to_display
        self._seq = sequence
        self._start_point = 0
        self._number_to_display = number_to_display
    
    def __iter__(self):
        return self
    
    def __next__(self):  
        if self._start_point < len(self._seq):
            if self._number_to_display >= len(self._seq):
                self._start_point = len(self._seq) + 1
                return self._seq
            if self._end_point <= len(self._seq):
                items_to_display = self._seq[self._start_point:self._end_point]
                self._start_point += self._number_to_display
                self._end_point += self._number_to_display
                return items_to_display
             
            items_to_display = self._seq[self._start_point:] 
            self._start_point += self._number_to_display      
            return items_to_display      
        raise StopIteration
    
