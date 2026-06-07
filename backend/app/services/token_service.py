import secrets
from datetime import datetime, timedelta, timezone
from app.config import get_settings

# 内存存储 token（生产环境应使用 Redis）
_token_store: dict[str, dict] = {}

TOKEN_EXPIRY_HOURS = 24


def generate_token(user_id: str, device_id: str) -> str:
    """生成随机 token 并存储"""
    token = secrets.token_urlsafe(32)
    _token_store[token] = {
        "user_id": user_id,
        "device_id": device_id,
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }
    return token


def verify_token(token: str) -> dict | None:
    """验证 token，返回用户信息或 None"""
    data = _token_store.get(token)
    if not data:
        return None

    if datetime.now(timezone.utc) > data["expires_at"]:
        del _token_store[token]
        return None

    return data


def revoke_token(token: str) -> bool:
    """撤销 token"""
    if token in _token_store:
        del _token_store[token]
        return True
    return False


def cleanup_expired_tokens():
    """清理过期 token"""
    now = datetime.now(timezone.utc)
    expired = [t for t, d in _token_store.items() if now > d["expires_at"]]
    for t in expired:
        del _token_store[t]
