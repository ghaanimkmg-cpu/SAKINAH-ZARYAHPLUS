from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1.nis import auth_test, kyc, eligibility, profile, preferences, interests, matchflows, conversations, reports, admin_reviews, considered_few, dev, niyyah, values, mirror, portrait, readiness

api_router = APIRouter()
api_router.include_router(health.router, tags=['health'])
api_router.include_router(auth_test.router, prefix="/nis/auth", tags=['auth'])
api_router.include_router(kyc.router, prefix="/nis/kyc", tags=['kyc'])
api_router.include_router(eligibility.router, prefix="/nis/eligibility", tags=['eligibility'])
api_router.include_router(readiness.router, prefix="/nis/readiness", tags=['readiness'])
api_router.include_router(niyyah.router, prefix="/nis/niyyah", tags=['niyyah'])
api_router.include_router(values.router, prefix="/nis/values", tags=['values'])
api_router.include_router(mirror.router, prefix="/nis/mirror", tags=['mirror'])
api_router.include_router(portrait.router, prefix="/nis/portrait", tags=['portrait'])
api_router.include_router(profile.router, prefix="/nis/profile", tags=['profile'])
api_router.include_router(preferences.router, prefix="/nis/preferences", tags=['preferences'])
api_router.include_router(considered_few.router, prefix="/nis/considered-few", tags=['considered_few'])
api_router.include_router(interests.router, prefix="/nis", tags=['interests'])
api_router.include_router(matchflows.router, prefix="/nis/matchflows", tags=['matchflows'])
api_router.include_router(conversations.router, prefix="/nis/conversations", tags=['conversations'])
api_router.include_router(reports.router, prefix="/nis/reports", tags=['reports'])
api_router.include_router(admin_reviews.router, prefix="/nis/admin/reviews", tags=['admin_reviews'])
api_router.include_router(dev.router, prefix="/nis/dev", tags=['dev'])

