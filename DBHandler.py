from sqlalchemy import create_engine
import dataretrieval_hospitals as dh
import dataretrieval_schools as ds
import dataretrieval_oev as doev
import dataretrieval_metadata as dm
import pandas as pd
import etl_pipeline as etl
import gis_calculations as gisc

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

def saveAllPLZToDbRaw():
    df = dm.scrapeAllPLZReturnAsDf()
    df.to_sql('plz_kanton_mapping', con=engine, if_exists='replace', index=False)
    print('Inserting PLZ Done')

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
    df.to_sql('hospitals_transformed', con=engine, if_exists='append', index=False)
    print('Inserting Hospitals Transformed Done')

def saveSchoolsToDbTransformed():
    df = etl.transformSchoolData()
    df.to_sql('schools_transformed', con=engine, if_exists='append', index=False)
    print('Inserting Schools Transformed Done')

def saveOevToDbTransformed():
    df = etl.transformOevData()
    df.to_sql('oev_transformed', con=engine, if_exists='append', index=False)
    print('Inserting OEV Transformed Done')

def retrieveIsochronesHospitalsZH():
    df = pd.read_sql("SELECT * FROM hospitals_final_zh_isochrones_v2", engine)
    return df

def retrieveIsochronesSchoolsZH():
    df = pd.read_sql("SELECT * FROM schools_final_zh_isochrones_v2", engine)
    return df

def retrieveOevDataTransformed():
    df = pd.read_sql("SELECT * FROM oev_transformed", engine)
    return df

def retrieveOevDataFinalZH():
    df = pd.read_sql("SELECT * FROM oev_final_zh", engine)
    return df

def retrieveSchoolDataFinalZH():
    df = pd.read_sql("SELECT * FROM schools_final_zh", engine)
    return df

def retrieveHospitalDataFinalZH():
    df = pd.read_sql("SELECT * FROM hospitals_final_zh", engine)
    return df

def saveOevInHospitalIsochronesZH():
    df = gisc.calculateOevInHospitalIsochronesZH()
    df.to_sql('oev_in_hospital_isochrones_zh', con=engine, if_exists='append', index=False)
    print('Inserting Oev in Hospital-Isochrones finished')

def saveOevInSchoolIsochronesZH():
    df = gisc.calculateOevInSchoolIsochronesZH()
    df.to_sql('oev_in_school_isochrones_zh', con=engine, if_exists='append', index=False)
    print('Inserting Oev in School-Isochrones finished')

def retrieveOevInHospitalIsochronesZHEnriched():
    df = pd.read_sql("SELECT * FROM oev_in_hospitals_isochrones_zh_no_dupl_enriched", engine)
    return df

def retrieveOevInSchoolsIsochronesZHEnriched():
    df = pd.read_sql("SELECT * FROM oev_in_schools_isochrones_zh_no_dupl_enriched", engine)
    return df