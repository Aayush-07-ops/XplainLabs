import io
import pandas as pd

LOAN_CSV = """Loan_ID,Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,Loan_Status
LP001002,Male,No,0,Graduate,No,5849,0,,360,1,Urban,Y
LP001003,Male,Yes,1,Graduate,No,4583,1508,128,360,1,Rural,N
LP001005,Male,Yes,0,Graduate,Yes,3000,0,66,360,1,Urban,Y
LP001006,Male,Yes,0,Not Graduate,No,2583,2358,120,360,1,Urban,Y
LP001008,Male,No,0,Graduate,No,6000,0,141,360,1,Urban,Y
LP001011,Male,Yes,2,Graduate,Yes,5417,4196,267,360,1,Urban,Y
LP001013,Male,Yes,0,Not Graduate,No,2333,1516,95,360,1,Urban,Y
LP001014,Male,Yes,3,Graduate,No,3036,2504,158,360,0,Semiurban,N
LP001018,Male,Yes,2,Graduate,No,4006,1526,168,360,1,Urban,Y
LP001020,Male,Yes,1,Graduate,No,12841,10968,349,360,1,Semiurban,N
LP001024,Male,Yes,2,Graduate,No,3200,700,70,360,1,Urban,Y
LP001027,Male,Yes,2,Graduate,Yes,2500,1840,109,360,1,Urban,Y
LP001028,Male,Yes,2,Graduate,No,3073,8106,200,360,1,Urban,Y
LP001029,Male,No,0,Graduate,No,1853,2840,114,360,1,Rural,N
LP001030,Male,Yes,2,Graduate,No,1299,1086,17,120,1,Urban,Y
LP001032,Male,No,0,Graduate,No,4950,0,125,360,1,Urban,Y
LP001034,Male,No,1,Not Graduate,No,3596,0,100,240,,Urban,Y
LP001036,Female,No,0,Graduate,No,3510,0,76,360,0,Urban,N
LP001038,Male,Yes,0,Not Graduate,No,4887,0,133,360,1,Rural,N
LP001041,Male,Yes,0,Graduate,Yes,2600,3500,115,,1,Urban,Y
LP001043,Male,Yes,0,Not Graduate,No,7660,0,104,360,0,Urban,N
LP001046,Male,Yes,1,Graduate,No,5955,5625,315,360,1,Urban,Y
LP001047,Male,Yes,0,Not Graduate,No,2600,1911,116,360,0,Semiurban,N
LP001052,Male,Yes,1,Graduate,Yes,3717,2925,151,360,,Semiurban,N
LP001066,Male,Yes,0,Graduate,Yes,9560,0,191,360,1,Semiurban,Y
LP001068,Male,Yes,0,Graduate,No,2799,2253,122,360,1,Semiurban,Y
LP001073,Male,Yes,2,Not Graduate,No,4226,1040,110,360,1,Urban,Y
LP001086,Male,No,0,Not Graduate,No,1442,0,35,360,1,Urban,N
LP001087,Female,No,2,Graduate,Yes,3750,2083,120,360,1,Semiurban,Y
LP001095,Male,No,0,Graduate,No,3167,0,74,360,1,Urban,N
LP001097,Male,No,1,Graduate,Yes,4692,0,106,360,1,Rural,N
LP001098,Male,Yes,0,Graduate,No,3500,1667,114,360,1,Semiurban,Y
LP001100,Male,No,3,Graduate,No,12500,3000,320,360,1,Rural,N
LP001112,Female,Yes,0,Graduate,No,3667,1459,144,360,1,Semiurban,Y
LP001114,Male,No,0,Graduate,No,4166,7210,184,360,1,Urban,Y
LP001116,Male,No,0,Not Graduate,No,3748,1668,110,360,1,Semiurban,Y
LP001119,Male,No,0,Graduate,No,3600,0,80,360,1,Urban,N
LP001120,Male,No,0,Graduate,No,1800,1213,47,360,1,Urban,Y
LP001123,Male,Yes,0,Graduate,No,2400,0,75,360,,Urban,Y
LP001131,Male,Yes,0,Graduate,No,3941,2336,134,360,1,Semiurban,Y
LP001136,Male,Yes,0,Not Graduate,Yes,4695,0,96,,1,Urban,Y
LP001137,Female,No,0,Graduate,No,3410,0,88,,1,Urban,Y
LP001146,Female,Yes,0,Graduate,No,2645,3440,120,360,0,Urban,N
LP001151,Female,No,0,Graduate,No,4000,2275,144,360,1,Semiurban,Y
LP001155,Female,Yes,0,Not Graduate,No,1928,1644,100,360,1,Semiurban,Y
LP001164,Female,No,0,Graduate,No,4230,0,112,360,1,Semiurban,N
"""

STUDENT_CSV = """Student_ID,Gender,Attendance,CGPA,Backlogs,Credits_Completed,Department,Hosteller,Eligible
STU001,Male,88,8.4,0,24,CSE,Yes,Yes
STU002,Female,72,7.1,1,22,IT,No,Yes
STU003,Male,65,6.2,2,20,EEE,Yes,No
STU004,Female,90,9.0,0,28,CSE,No,Yes
STU005,Male,55,5.6,3,16,ME,Yes,No
STU006,Female,78,7.8,0,23,ECE,No,Yes
STU007,Male,60,6.0,2,18,CE,Yes,No
STU008,Female,85,8.1,1,25,IT,No,Yes
STU009,Male,92,9.2,0,30,CSE,Yes,Yes
STU010,Female,68,6.7,2,19,EEE,No,No
STU011,Male,75,7.4,1,21,ME,Yes,Yes
STU012,Female,58,5.9,3,17,CE,No,No
STU013,Male,82,8.0,0,26,ECE,Yes,Yes
STU014,Female,70,7.0,1,22,IT,Yes,Yes
STU015,Male,62,6.1,2,18,ME,No,No
"""

def load_loan_df() -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(LOAN_CSV))
    # normalize blanks to NaN
    df = df.replace({"": None})
    return df

def load_student_df() -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(STUDENT_CSV))
    df = df.replace({"": None})
    return df