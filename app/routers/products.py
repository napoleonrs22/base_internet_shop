from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.database import get_db


router = APIRouter(
    prefix="/products",
    tags=["products"],
)



@router.get('/', response_model=list[ProductSchema])
async def get_all_products(db: Session = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    products = db.scalars(stmt).all()
    return products

@router.post('/', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db) ):


    stmt = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                        CategoryModel.is_active == True)
    
    category = db.scalars(stmt).first()

    if not category:
        raise HTTPException(status_code=400, detail="Категория не найдена или не активна")
    db_category = ProductModel(**product.model_dump(), is_active=True)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get('/category/{category_id}', response_model=list[ProductSchema])
async def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список товаров по ID категории.
    """
    stmt = select(CategoryModel).where(CategoryModel.id == category_id,
                                        CategoryModel.is_active == True)    
    category = db.scalars(stmt).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found or inactive")
    
    stmt_products = select(ProductModel).where(ProductModel.category_id == category_id,
                                                ProductModel.is_active == True)
    products = db.scalars(stmt_products).all()
    
    return products

@router.get('/{product_id}', response_model=ProductSchema)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о товаре по ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,
                                       ProductModel.is_active == True)
    product = db.scalars(stmt).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or inactive")
    
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                                 CategoryModel.is_active == True)
    category = db.scalars(stmt_category).first()
    
    if not category:
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    
    return product

@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """
    Обновляет информацию о товаре по ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,
                                        ProductModel.is_active == True)
    
    db_product = db.scalars(stmt).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or inactive")
    
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                                    CategoryModel.is_active == True)
    category = db.scalars(stmt_category).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(
            name=product.name,
            description=product.description,
            price=product.price,
            image_url=product.image_url,
            stock=product.stock,
            category_id=product.category_id
        )
    )
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete('/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаляет товар по ID (логическое удаление).
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,
                                        ProductModel.is_active == True)
    db_product = db.scalars(stmt).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or inactive")
    
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(is_active=False)
    )
    db.commit()
    
    return {"status": "success", "message": "Product marked as inactive"}