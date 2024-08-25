import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database engine
engine = create_engine('sqlite:///restaurant_data.db')
Base = declarative_base()

# Define database models
class StoreStatus(Base):
    __tablename__ = 'store_status'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    status = Column(String)
    timestamp_utc = Column(DateTime)

class BusinessHours(Base):
    __tablename__ = 'business_hours'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    day_of_week = Column(Integer)
    start_time_local = Column(String)
    end_time_local = Column(String)

class Timezone(Base):
    __tablename__ = 'timezone'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timezone_str = Column(String)

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Import data from CSVs
def import_data():
    store_status = pd.read_csv('store_status.csv')
    store_status['timestamp_utc'] = pd.to_datetime(store_status['timestamp_utc'])
    store_status.to_sql('store_status', engine, if_exists='replace', index=False)

    business_hours = pd.read_csv('business_hours.csv')
    business_hours.to_sql('business_hours', engine, if_exists='replace', index=False)

    timezone = pd.read_csv('timezone.csv')
    timezone.to_sql('timezone', engine, if_exists='replace', index=False)

if __name__ == '__main__':
    import_data()