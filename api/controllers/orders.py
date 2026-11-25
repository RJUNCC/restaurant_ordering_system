from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import customers as customer_model, menu as menu_model, order_details as detail_model
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal


def create(db: Session, request):
    new_item = model.Order(
        customer_id=request.customer_id,
        order_type=request.order_type,
        promotion_id=request.promotion_id,
        payment_id=request.payment_id,
        description=request.description
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def checkout(db: Session, request):
    customer = db.query(customer_model.Customer).filter(customer_model.Customer.phone == request.phone).first()
    if customer is None:
        customer = customer_model.Customer(
            name=request.name,
            phone=request.phone,
            address=request.address,
            email=request.email
        )
        db.add(customer)

    subtotal = Decimal("0")
    for item in request.items:
        menu_item = db.query(menu_model.Menu).filter(menu_model.Menu.id == item.menu_id).first()
        if menu_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item {item.menu_id} not found")
        subtotal += menu_item.price * item.amount

    order = model.Order(
        customer=customer,
        order_type=request.order_type,
        description=request.description,
        total_price=subtotal
        )

    for item in request.items:
        order.order_details.append(detail_model.OrderDetail(menu_id=item.menu_id, amount=item.amount))
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
    except SQLAlchemyError as e:
        db.rollback()
    return order
