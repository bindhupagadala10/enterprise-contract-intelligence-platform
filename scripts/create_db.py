from app.db.database import Base, engine

import app.db.models.user

Base.metadata.create_all(bind=engine)

print("Database created.")