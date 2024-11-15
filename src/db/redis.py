import aioredis
from src.config import Config


JTI_EXPIRY = 3600

token_block_list = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)


async def add_jti_to_block_list(jti: str) -> None:
    await token_block_list.set(name=jti, value="", ex=JTI_EXPIRY)


async def is_token_in_block_list(jti: str)->bool:
    jti = await token_block_list.get(jti)
    
    return jti is not None