from fastapi import APIRouter
from .controller import HHMockController

router = APIRouter(prefix="/hh")


@router.get("/resumes/{resume_id}")
async def get_hh_resume_data_mock(resume_id: str):
    fake_resume = HHMockController.generate_random_resume_data()
    fake_resume["id"] = resume_id
    return fake_resume
