from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("")
async def get_tasks():
    return "A lot of tasks"