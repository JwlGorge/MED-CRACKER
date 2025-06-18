
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question, student
import sys  # Add this for flush
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel




app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Tanjiro"})

@app.get("/test", response_class=HTMLResponse)
async def testPage(request: Request):
    return templates.TemplateResponse("BIOtest.html", {"request": request})


@app.get("/questions/{subject}")
def get_questions(subject: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.Subject == subject).all()



@app.get("/quiz")
def show_questions(request: Request, db: Session = Depends(get_db)):
    questions = db.query(Question).all()

    try:
        # Debugging print that will definitely show
        print("DEBUG: Entered /quiz endpoint", file=sys.stderr)
        sys.stderr.flush()
        
        questions = db.query(Question).filter(Question.Subject == "Biology").all()
        print(f"DEBUG: Found {len(questions)} questions", file=sys.stderr)
        sys.stderr.flush()
        
        if not questions:
            print("DEBUG: No questions found!", file=sys.stderr)
            sys.stderr.flush()
        
        questions_data = [
            {
                "id": q.id,
                "text": q.Question,
                "options": [q.Option_1, q.Option_2, q.Option_3, q.Option_4],
                "correct": q.Correct_option,
                "difficulty": q.Toughness
            }
            for q in questions
        ]
        
        print(f"DEBUG: First question: {questions_data[0] if questions_data else 'None'}", file=sys.stderr)
        sys.stderr.flush()
        
        return templates.TemplateResponse(
            "quiz.html",
            {
                "request": request,
                "questions": questions_data,
                "total": len(questions_data)
            }
        )
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.stderr.flush()
        raise












#Signup Endpoint
class SignupRequest(BaseModel):
    username: str
    password: str
# @app.post("/signup")
# def signup(request: SignupRequest, db: Session = Depends(get_db)):
#     username = request.username
#     password = request.password

#     existing_user = db.query(student).filter(student.username == username).first()
    
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     new_user = student(username=username, password=password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User created successfully", "user_id": new_user.id}



# Login Endpoint
class SignupRequest(BaseModel):
    username: str
    password: str

@app.get("/login", response_class=HTMLResponse)
def login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request": request})


@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(student).filter(student.username == username).first()
    print("USER DEAILS ENTERED\n")
    if user and user.password == password:
        print("umbiyilla")
        return JSONResponse(status_code=200, content={"message": f"Welcome {username}!"})
    
    else:
        print("umbiyalloo")
        return JSONResponse(status_code=401, content={"detail": "Invalid username or password"})

# @app.post("/login")
# def login(request: SignupRequest, db: Session = Depends(get_db)):
#     username = request.username
#     password = request.password
#     user = db.query(student).filter(student.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.password != password:
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     return {"message": "Login successful", "user_id": user.id}


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request:Request):
    return templates.TemplateResponse("signup.html",{"request": request})


@app.post("/signup")
def handle_signup(
    username: str = Form(...),
    password: str = Form(...),
    number: str = Form(...),
    duration: int = Form(...),
    db: Session = Depends(get_db)
):
    print("USER DETAILS ACCEPTED\n")

    existing_user = db.query(student).filter(student.username == username).first()
    if existing_user:
        print("Username already exists")
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user record with all fields
    new_user = student(
        username=username,
        password=password,
        number=number,
        duration=duration
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("User created successfully")
    return {"message": "User created successfully", "user_id": new_user.id}
