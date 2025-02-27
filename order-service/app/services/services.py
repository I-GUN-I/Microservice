from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def get_all_approvals(db: Session):
    """Retrieve all approvals, ordered by most recently receive."""
    return db.query(models.Approval).order_by(models.Approval.order_receive.desc()).all()

def get_approval_by_id(db: Session, approval_id: int):
    """Retrieve an approval by its ID."""
    return db.query(models.Approval).filter(models.Approval.id == approval_id).first()

def get_approval_by_order_id(db: Session, approval_id: int):
    """Retrieve an approval by order's ID."""
    return db.query(models.Approval).filter(models.Approval.id == approval_id).first()

def update_approval_status(db: Session, approval_id: int, approval_update: schemas.ApprovalUpdate):
    """Update the status of an approval."""
    # Retrieve the approval record by ID
    approval = db.query(models.Approval).filter(models.Approval.id == approval_id).first()

    if not approval:
        raise ValueError(f"Approval with ID {approval_id} not found.")

    # Update the status
    approval.order_status = approval_update.order_status
    approval.approval_date = func.now()  # Set the approval date when the status is updated

    # Commit the changes to the database
    db.commit()
    db.refresh(approval)

    return approval
