from fastapi import APIRouter, Header, HTTPException
from services.auth_factory import get_auth_service

router = APIRouter()

@router.post("/confido-health/api/v1/auth", tags=["auth"])
async def generate_token(x_source_type: str = Header(...)):
    try:
        source = x_source_type.lower()
        source_service = get_auth_service(source)
        result = await source_service.generate_access_token()
        return {"source": source, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
