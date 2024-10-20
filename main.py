# create comments for the code by explaining what each and everyhting is doing

# Importing the necessary libraries


from fastapi import FastAPI, HTTPException # Importing FastAPI and HTTPException from fastapi
from pydantic import BaseModel # Importing BaseModel from pydantic
from typing import List, Optional # Importing List and Optional from typing
from uuid import UUID, uuid4 # Importing UUID and uuid4 from uuid

app = FastAPI()  # Creating an instance of FastAPI


#Pydentic Model
class Task(BaseModel): # Creating a class Task that inherits from BaseModel
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False



tasks = []  # Creating an empty list called tasks



@app.post("/tasks/", response_model=Task)   # @app.post is a decorator that tells FastAPI that the function below is a POST request handler, the /tasks/ is the endpoint of the API and response_model=Task is the response model of the API 
def create_task(task: Task): # Creating a function called create_task that takes in a parameter called task
    task.id = uuid4() # Assigning a random UUID to the task id
    tasks.append(task) # Appending the task to the tasks list
    return task # Returning the task



@app.get("/tasks/", response_model=List[Task]) # @app.get is a decorator that tells FastAPI that the function below is a GET request handler, the /tasks/ is the endpoint of the API and response_model=List[Task] is the response model of the API
def read_tasks(): # Creating a function called read_tasks
    return tasks # Returning the tasks list



@app.get("/tasks/{task_id}", response_model=Task) # @app.get is a decorator that tells FastAPI that the function below is a GET request handler, the /tasks/{task_id} is the endpoint of the API in which the {task_id} is a path parameter and response_model=Task is the response model of the API
def read_task(task_id: UUID): # Creating a function called read_task that takes in a parameter called task_id
    for task in tasks: # Looping through the tasks list
        if task.id == task_id:  # Checking if the task id is equal to the task_id
            return task     # Returning the task
        
    raise HTTPException(status_code=404, detail="Task not found") # Raise an HTTPException with a status code of 404 and a detail of "Task not found"



@app.put("/tasks/{task_id}", response_model=Task) # @app.put is a decorator that tells FastAPI that the function below is a PUT request handler, the /tasks/{task_id} is the endpoint of the API in which the {task_id} is a path parameter and response_model=Task is the response model of the API
def update_task(task_id: UUID, task_update: Task): # Creating a function called update_task that takes in two parameters called task_id and task_update
    for idx, task in enumerate(tasks): # Looping through the tasks list, the enumerate function returns the index and the value of the list
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task) # @app.delete is a decorator that tells FastAPI that the function below is a DELETE request handler, the /tasks/{task_id} is the endpoint of the API in which the {task_id} is a path parameter and response_model=Task is the response model of the API
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__": # If the name of the module is equal to __main__ 
    import uvicorn # Importing uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000) # Running the FastAPI app using uvicorn on host