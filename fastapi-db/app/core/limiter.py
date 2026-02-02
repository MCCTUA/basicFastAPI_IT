from slowapi import Limiter
from slowapi.util import get_remote_address

# สร้าง Limiter instance
# key_func=get_remote_address หมายถึงจะจำกัดการเรียกใช้งานโดยดูจาก IP Address ของผู้เรียก
limiter = Limiter(key_func=get_remote_address)
