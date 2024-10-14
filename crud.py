from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import UserModel, TaskModel
from schema import UserCreate, TaskCreate  
from security import hash_password

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

# Create user
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback() 
        raise ValueError("Username or email already registered.")

# Get all tasks for a user
def get_tasks(db: Session, user_id: str):
    return db.query(TaskModel).filter(TaskModel.owner_id == user_id).all()

# Create a new task
def create_task(db: Session, task: TaskCreate, user_id: str):
    new_task = TaskModel(**task.dict(), owner_id=user_id)
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except IntegrityError:
        db.rollback()  # Rollback in case of an error
        raise ValueError("Task with the same title already exists.")  # Adjust message as needed

# Get a task by ID
def get_task(db: Session, task_id: str, user_id: str):
    return db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.owner_id == user_id).first()

# Update an existing task
def update_task(db: Session, task_id: str, user_id: str, task: TaskCreate):
    existing_task = get_task(db, task_id, user_id)
    
    if existing_task is None:
        return None  

    
    existing_task.title = task.title
    existing_task.description = task.description

    # Save changes to the database
    try:
        db.commit()
        db.refresh(existing_task)
    except IntegrityError:
        db.rollback()  # Rollback in case of an error
        raise ValueError("Error updating task. Title may already be in use.")  # Adjust message as needed

    return existing_task

# Delete a task
def delete_task(db: Session, task_id: str, user_id: str):
    task = get_task(db, task_id, user_id)
    if task:
        db.delete(task)
        db.commit()
        return task
    raise ValueError("Task not found or not owned by the user.")  # Raise an exception if the task is not found
