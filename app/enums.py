from enum import Enum


class UserRole(str, Enum):

    ADMIN = "Admin"

    WAREHOUSE_MANAGER = "Warehouse Manager"


class TransferStatus(str, Enum):

    PENDING = "Pending"

    APPROVED = "Approved"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"