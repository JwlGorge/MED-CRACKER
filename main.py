
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models import Question
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware

# app=FastAPI()

# templates = Jinja2Templates(directory="templates")

# ######################################################################################################################################################





# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, restrict this
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )




# #######################################################################################################################################################






# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "name": "Tanjiro"})

# @app.get("/test", response_class=HTMLResponse)
# async def testPage(request: Request):
#     return templates.TemplateResponse("BIOtest.html", {"request": request})



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/questions/{subject}")
# def get_questions(subject: str, db: Session = Depends(get_db)):
#     return db.query(Question).filter(Question.Subject == subject).all()

# ######################################################################################################################################

# @app.get("/quiz")
# def show_questions(request: Request, db: Session = Depends(get_db)):
#     questions = db.query(Question).all()
#     return templates.TemplateResponse("qstesting.html", {
#         "request": request,
#         "questions": questions
#     })

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
import sys  # Add this for flush
from fastapi.responses import HTMLResponse




app = FastAPI()
templates = Jinja2Templates(directory="templates")

<<<<<<< Updated upstream
=======

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> Stashed changes

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Tanjiro"})

@app.get("/test", response_class=HTMLResponse)
async def testPage(request: Request):
    return templates.TemplateResponse("BIOtest.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def show_quiz(request: Request, db: Session = Depends(get_db)):
    try:
<<<<<<< Updated upstream
        yield db
    finally:
        db.close()

@app.get("/questions/{subject}")
def get_questions(subject: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.Subject == subject).all()


@app.get("/quiz")
def show_questions(request: Request, db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return templates.TemplateResponse("qstesting.html", {
        "request": request,
        "questions": questions
    })
=======
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
>>>>>>> Stashed changes
