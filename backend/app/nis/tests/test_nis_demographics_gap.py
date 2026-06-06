import pytest
from app.nis.services.considered_few_service import NISConsideredFewService

@pytest.mark.xfail(reason="Demographic gap must be fixed before production")
def test_considered_few_demographic_production_readiness():
    """
    This test serves as a blocking mechanism and documentation for the Phase K
    demographics gap. It asserts that considered-few uses static demographic
    defaults (e.g. age=25, location="Unknown") instead of a real database model.
    
    Before the matching system goes to production, the `NISDemographicProfile`
    (or equivalent KYC profile) must be implemented and queried here.
    
    Remove the xfail marker when this gap is resolved.
    """
    # For now, this test explicitly fails because we know the static defaults exist.
    assert False, "Considered-few currently relies on static age/location defaults instead of a DB model."
