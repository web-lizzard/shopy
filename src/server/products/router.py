from fastapi import APIRouter


router = APIRouter(prefix='/products')


@router.get('/')
def get_products():
    return []