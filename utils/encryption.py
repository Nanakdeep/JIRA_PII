import hashlib
import hmac
import json


def calculate_sha256(data: bytes) -> str:
    """Calculate the SHA256 hash value of the input data.

    Args:
        data (bytes): The data to be hashed.

    Returns:
        str: The hexadecimal representation of the SHA256 hash value.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    sha256_hex = sha256_hash.hexdigest()

    return sha256_hex


def calculate_hmac(secret_key: bytes, response: dict) -> str:
    """
    Calculates the HMAC (hash-based message authentication code) of the provided
    file bytes using the provided secret key and SHA-256 hash algorithm.

    Args:
        secret_key (bytes): The secret key to use for generating the HMAC.
        file_bytes (bytes): The bytes of the file to generate the HMAC for.

    Returns:
        str: The hexadecimal representation of the computed HMAC.
    """

    request_body_json = json.dumps(response).encode("utf-8")

    hash_algorithm = hashlib.sha256
    computed_hmac = hmac.new(secret_key, request_body_json, hash_algorithm).hexdigest()

    return computed_hmac
