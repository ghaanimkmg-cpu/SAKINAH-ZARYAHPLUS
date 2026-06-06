from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1.nis import auth_test, kyc, eligibility, profile, preferences, interests, matchflows

api_router = APIRouter()
api_router.include_router(health.router, tags=['health'])
api_router.include_router(auth_test.router, prefix="/nis/auth", tags=['auth'])
api_router.include_router(kyc.router, prefix="/nis/kyc", tags=['kyc'])
api_router.include_router(eligibility.router, prefix="/nis/eligibility", tags=['eligibility'])
api_router.include_router(profile.router, prefix="/nis/profile", tags=['profile'])
api_router.include_router(preferences.router, prefix="/nis/preferences", tags=['preferences'])
api_router.include_router(interests.router, prefix="/nis", tags=['interests'])
api_router.include_router(matchflows.router, prefix="/nis/matchflows", tags=['matchflows'])

