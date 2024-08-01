import re

# regex phone number
def validate_phone_number(phone_number):
    pattern = r"^\+98912\d{7}$"
    return re.match(pattern, phone_number) is not None


print(validate_phone_number("+989123456789"))  # True
print(validate_phone_number("+989131234561"))   # False


# regex national code
def validate_national_code(national_code):
    pattern = r"^\d{10}$"
    return re.match(pattern, national_code) is not None


print(validate_national_code("1234567890"))  # True
print(validate_national_code("12345"))       # False


# regex persian or latin name
def validate_name(name):
    pattern = r"^[a-zA-Z\u0600-\u06FF\s]+$"
    return re.match(pattern, name) is not None


print(validate_name("Ali Reza"))           # True
print(validate_name("علیرضا"))              # True
print(validate_name("Ali123"))             # False