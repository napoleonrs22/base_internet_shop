from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
)



@router.get('/')
async def get_all_products():
    """
    Возвращает список всех товаров.
    """
    return {"message": "Список всех товаров (заглушка)"}

@router.post('/')
async def create_product():
    """
    Создает новый товар.
    """
    return {"message": "Товар создан (заглушка)"}

@router.get('/category/{category_id}')
async def get_products_by_category(category_id: int):
    """
    Возвращает список товаров по ID категории.
    """
    return {"message": f"Список товаров для категории с ID {category_id} (заглушка)"}

@router.get('/{product_id}')
async def get_product_by_id(product_id: int):
    """
    Возвращает информацию о товаре по ID.
    """
    return {"message": f"Информация о товаре с ID {product_id} (заглушка)"}

@router.put('/{product_id}')
async def update_product(product_id: int):
    """
    Обновляет информацию о товаре по ID.
    """
    return {"message": f"Товар с ID {product_id} обновлен (заглушка)"}

@router.delete('/{product_id}')
async def delete_product(product_id: int):
    """
    Удаляет товар по ID.
    """
    return {"message": f"Товар с ID {product_id} удален (заглушка)"}