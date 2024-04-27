from sqlalchemy import create_engine
import dataretrieval_hospitals as dh
import dataretrieval_schools as ds
import dataretrieval_oev as doev
import pandas as pd
import etl_pipeline as etl

DATABASE_URL = "postgresql://admin:Yasha99@localhost:5432/geodaten_p1"
engine = create_engine(DATABASE_URL)

def saveHospitalsToDbRaw():
    df = dh.scrape_all_hospitals_return_asDf()
    df.to_sql('hospitals_raw', con=engine, if_exists='replace', index=False)
    print('Inserting Hospitals Done')

def saveSchoolsToDbRaw():
    df = ds.scrape_all_schools_return_asDf()
    df.to_sql('schools_raw', con=engine, if_exists='replace', index=False)
    print('Inserting Schools Done')

def saveOevToDbRaw():
    df = doev.scrapeAllOevReturnAsDf()
    df.to_sql('oev_raw', con=engine, if_exists='replace', index=False)
    print('Inserting OeV Done')

def retrieveHospitalDataRaw():
    df = pd.read_sql("SELECT * FROM hospitals_raw", engine)
    return df

def retrieveSchoolDataRaw():
    df = pd.read_sql("SELECT * FROM schools_raw", engine)
    return df

def retrieveOevDataRaw():
    df = pd.read_sql("SELECT * FROM oev_raw", engine)
    return df

def saveHospitalsToDbTransformed():
    df = etl.transformHospitalData()
    df.to_sql('hospitals_transformed', con=engine, if_exists='replace', index=False)
    print('Inserting Hospitals Transformed Done')

def saveSchoolsToDbTransformed():
    df = etl.transformSchoolData()
    df.to_sql('schools_transformed', con=engine, if_exists='replace', index=False)
    print('Inserting Schools Transformed Done')

def saveOevToDbTransformed():
    df = etl.transformOevData()
    df.to_sql('oev_transformed', con=engine, if_exists='replace', index=False)
    print('Inserting OEV Transformed Done')