from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.models import User
from app.utils import image_to_embedding
import face_recognition
import pickle
from contextlib import contextmanager

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register-face")
def register_face(username: str = Form(...), image: str = Form(...)):
    embedding = image_to_embedding(image)
    if embedding is None:
        raise HTTPException(status_code=400, detail="No se detectó rostro.")
    
    with get_db() as db:
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Usuario ya registrado.")
        
        emb_serialized = pickle.dumps(embedding)  # Considera usar otro método si es posible
        user = User(username=username, embedding=emb_serialized)
        db.add(user)
        db.commit()
    
    return {"msg": "Usuario registrado exitosamente"}

@app.post("/verify-face")
def verify_face(image: str = Form(...)):
    embedding = image_to_embedding(image)
    if embedding is None:
        raise HTTPException(status_code=400, detail="No se detectó rostro.")
    
    with get_db() as db:
        users = db.query(User).all()
        for user in users:
            db_embedding = pickle.loads(user.embedding)  # Considera usar otro método si es posible
            matches = face_recognition.compare_faces([db_embedding], embedding)
            if matches[0]:
                return {"user_id": user.id, "username": user.username}
    
    raise HTTPException(status_code=401, detail="Usuario no reconocido")
