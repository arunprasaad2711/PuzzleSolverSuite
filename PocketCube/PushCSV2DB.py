import pandas as pd
from sqlalchemy import create_engine

# Database connection
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "pocketcube"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Read CSV
df = pd.read_csv("PocketCubeAtlas.csv")

# Push to PostgreSQL
df.to_sql("PocketCube", engine, if_exists="replace", index=False)

print(f"Done! {len(df)} rows imported.")