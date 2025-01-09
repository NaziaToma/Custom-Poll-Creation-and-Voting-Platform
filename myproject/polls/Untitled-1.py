s ="race a: caR"
s = s.lower()
s = ''.join(char for char in s if char.isalnum())


print(s)