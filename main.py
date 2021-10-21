import keys_management
import crypto

# keys_management.generate_keys()

private_key = keys_management.read_private_key()
public_key = private_key.public_key()

message = b'Hola bots'

encrypted_message = crypto.encrypt(message, public_key)
original_message = crypto.decrypt(encrypted_message, private_key)

print(encrypted_message)
print(original_message)