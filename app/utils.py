
# 3RD PARTY IMPORTS
from passlib.context import CryptContext

# LOCAL IMPORTS
...

# BUILT-IN IMPORTS
...



# Passlib algorithm setting
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Initial Hash Function
def hash(password:str) -> str:

    """This function has a password when a new user is created"""

    return pwd_context.hash(password)


# Comparator of passwords
def compare_pwds(plain_pwd:str, hashed_pwd:str) -> bool:

    """This function compares two passwords to see if they match according to the hash algorithm"""

    return pwd_context.verify(plain_pwd, hashed_pwd)







