import keys_management
import crypto

keys_management.generate_keys()

private_key = keys_management.read_key("private_key.pem")
public_key = private_key.public_key()

keys_management.write_key(public_key, "public.key.pem", False)