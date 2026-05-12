from datetime import datetime, timedelta

from jose import JWTError, jwt

from passlib.context import CryptContext


# 🔐 SECRET
SECRET_KEY = "splitai_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# 🔒 PASSWORD HASHING
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# 🔑 HASH PASSWORD
def hash_password(password):

    return pwd_context.hash(password)


# ✅ VERIFY PASSWORD
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# 🎟️ CREATE JWT TOKEN
def create_access_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )