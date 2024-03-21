from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if value:   
            self.value = value
        else:
            raise ValueError("Name field is required")

class Phone(Field):
    def __init__(self, value):
        if self.validate_phone(value):
            self.value = value
        else:
            print("Invalid phone number: must be 10 digits")
    
    def validate_phone(self, phone):
        return len(str(phone)) == 10
    
class Birthday(Field):
    def __init__(self, value):
        if self.validate_birthday(value):
            self.value = value
        else:
            raise
        ValueError("Invalid birthday format. DD.MM.YYYY required")

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)

    def __str__(self):
        phone_str = "; ".join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        birthday_dict = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        for name, record in self.data.items():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                    delta_days = (birthday_this_year - today).days

                    day_of_week = (today + timedelta(days=delta_days)).strftime("%A") if 0 <= delta_days < 7 else None

                if day_of_week in ["Saturday", "Sunday"]:
                    day_of_week = "Monday"

        if any(birthday_dict.values()):
            print("Birthdays in the next week:")
            for day, names in birthday_dict.items():
                if names:
                    print(f"{day}: {", ".join(names)}")
        else:
            print("No birthdays in the next week.")



# Function to parse user input
