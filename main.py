import keys_management

# keys_management.generate_keys()

private_key = keys_management.read_private_key()
public_key = private_key.public_key()

message = b'Hola bots'

encrypted_message = keys_management.encrypt(message, public_key)
original_message = keys_management.decrypt(encrypted_message, private_key)

print(encrypted_message)
print(original_message)