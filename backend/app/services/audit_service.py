from app.models.audit import AuditLog
from sqlalchemy.orm import Session
from typing import Optional
import json

def log_audit(db: Session, user_id: int, action: str, entity: str, entity_id: int, old_value: Optional[dict], new_value: Optional[dict], ip_address: str):
	audit = AuditLog(
		user_id=user_id,
		action=action,
		entity=entity,
		entity_id=entity_id,
		old_value=json.dumps(old_value) if old_value else None,
		new_value=json.dumps(new_value) if new_value else None,
		ip_address=ip_address
	)
	db.add(audit)
	db.commit()
