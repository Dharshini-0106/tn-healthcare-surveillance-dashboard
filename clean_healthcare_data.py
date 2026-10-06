import pandas as pd
from pathlib import Path

# Get the main project folder
project_path = Path(__file__).resolve().parent.parent

# Location of the raw Excel file
file_path = project_path / "data" / "TN_Healthcare_Performance_Raw.xlsx"

# Read the Disease_Data sheet
disease_df = pd.read_excel(
    file_path,
    sheet_name="Disease_Data"
)

# Display the first 5 rows
print(disease_df.head())

print("\n--- DATASET SHAPE ---")
print(disease_df.shape)

print("\n--- COLUMN NAMES ---")
print(disease_df.columns.tolist())

print("\n--- DUPLICATE RECORDS ---")
print(disease_df.duplicated().sum())

print("\n--- DUPLICATE RECORD ---")
print(disease_df[disease_df.duplicated(keep=False)])

# Remove exact duplicate records
disease_df = disease_df.drop_duplicates()
print("\n--- SHAPE AFTER REMOVING DUPLICATES ---")
print(disease_df.shape)

print("\n--- MISSING VALUES ---")
print(disease_df.isnull().sum())

print(disease_df.isnull().sum())

print(disease_df["Disease"].unique())

# Remove extra spaces from disease names
disease_df["Disease"] = disease_df["Disease"].str.strip()

print("\n--- DISEASES AFTER CLEANING SPACES ---")
print(disease_df["Disease"].unique())

# Standardize disease name capitalization
disease_df["Disease"] = disease_df["Disease"].str.title()

print("\n--- DISEASES AFTER CLEANING ---")
print(disease_df["Disease"].unique())

print("\n--- INVALID POSITIVE CASES ---")

invalid_positive = disease_df[
    disease_df["Positive Cases"] > disease_df["Samples Tested"]
]

print(invalid_positive)
print("Number of invalid records:", len(invalid_positive))

# Remove records where positive cases exceed samples tested
disease_df = disease_df[
    disease_df["Positive Cases"] <= disease_df["Samples Tested"]
]

print("\n--- SHAPE AFTER VALIDATION ---")
print(disease_df.shape)

print("\n--- DATA TYPES ---")
print(disease_df.dtypes)

# Calculate disease positivity rate
disease_df["Positivity Rate (%)"] = (
    disease_df["Positive Cases"] / disease_df["Samples Tested"]
) * 100

# Round positivity rate to 2 decimal places
disease_df["Positivity Rate (%)"] = disease_df["Positivity Rate (%)"].round(2)

print("\n--- SAMPLE POSITIVITY RATES ---")
print(
    disease_df[
        ["Disease", "Samples Tested", "Positive Cases", "Positivity Rate (%)"]
    ].head()
)

# Save cleaned Disease_Data
output_path = project_path / "output" / "TN_Healthcare_Disease_Cleaned.xlsx"

disease_df.to_excel(output_path, index=False)

print("\n--- CLEANED FILE SAVED ---")
print(output_path)

# ============================================================
# INSPECT OTHER SHEETS
# ============================================================

sheets = [
    "Emergency_Data",
    "Hospital_Data",
    "Doctor_Data",
    "Facility_Master"
]

for sheet in sheets:
    df = pd.read_excel(
        file_path,
        sheet_name=sheet
    )

    print("\n" + "=" * 60)
    print("SHEET:", sheet)
    print("=" * 60)

    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3))

    print("\nMissing values:")
    print(df.isnull().sum())

    # ============================================================
# VALIDATE OPERATIONAL TABLES
# ============================================================

print("\n" + "=" * 60)
print("VALIDATING OPERATIONAL TABLES")
print("=" * 60)

# Read the four operational tables
emergency_df = pd.read_excel(
    file_path,
    sheet_name="Emergency_Data"
)

hospital_df = pd.read_excel(
    file_path,
    sheet_name="Hospital_Data"
)

doctor_df = pd.read_excel(
    file_path,
    sheet_name="Doctor_Data"
)

facility_df = pd.read_excel(
    file_path,
    sheet_name="Facility_Master"
)


# ------------------------------------------------------------
# 1. DUPLICATE RECORDS
# ------------------------------------------------------------

print("\n--- DUPLICATES ---")

print(
    "Emergency_Data:",
    emergency_df.duplicated().sum()
)

print(
    "Hospital_Data:",
    hospital_df.duplicated().sum()
)

print(
    "Doctor_Data:",
    doctor_df.duplicated().sum()
)

print(
    "Facility_Master:",
    facility_df.duplicated().sum()
)


# ------------------------------------------------------------
# 2. IMPOSSIBLE BED VALUES
# ------------------------------------------------------------

print("\n--- INVALID BED VALUES ---")

invalid_beds = hospital_df[
    hospital_df["Occupied Beds"] > hospital_df["Bed Strength"]
]

print(invalid_beds)
print("Number of invalid records:", len(invalid_beds))


# ------------------------------------------------------------
# 3. IMPOSSIBLE DOCTOR VALUES
# ------------------------------------------------------------

print("\n--- INVALID DOCTOR VALUES ---")

invalid_doctors = doctor_df[
    doctor_df["Doctors Attended"] > doctor_df["Doctors Available"]
]

print(invalid_doctors)
print("Number of invalid records:", len(invalid_doctors))


# ------------------------------------------------------------
# 4. NEGATIVE VALUES
# ------------------------------------------------------------

print("\n--- NEGATIVE VALUES ---")

print(
    "Hospital negative values:",
    (hospital_df.select_dtypes("number") < 0).sum().sum()
)

print(
    "Emergency negative values:",
    (emergency_df.select_dtypes("number") < 0).sum().sum()
)

print(
    "Doctor negative values:",
    (doctor_df.select_dtypes("number") < 0).sum().sum()
)


# ------------------------------------------------------------
# 5. FACILITIES NOT IN MASTER
# ------------------------------------------------------------

print("\n--- FACILITY MASTER CHECK ---")

hospital_facilities = set(hospital_df["Facility Name"])
master_facilities = set(facility_df["Facility Name"])

missing_from_master = hospital_facilities - master_facilities

print(
    "Hospital facilities not found in Facility_Master:",
    len(missing_from_master)
)

print(missing_from_master)

# ============================================================
# CLEAN OPERATIONAL TABLES
# ============================================================

print("\n" + "=" * 60)
print("CLEANING OPERATIONAL TABLES")
print("=" * 60)


# ------------------------------------------------------------
# EMERGENCY DATA
# ------------------------------------------------------------

emergency_df = emergency_df.drop_duplicates()

print(
    "\nEmergency_Data after removing duplicates:",
    emergency_df.shape
)


# ------------------------------------------------------------
# HOSPITAL DATA
# ------------------------------------------------------------

hospital_df = hospital_df.drop_duplicates()

# Remove records where occupied beds exceed bed strength
hospital_df = hospital_df[
    hospital_df["Occupied Beds"] <= hospital_df["Bed Strength"]
]

print(
    "Hospital_Data after cleaning:",
    hospital_df.shape
)


# ------------------------------------------------------------
# DOCTOR DATA
# ------------------------------------------------------------

doctor_df = doctor_df.drop_duplicates()

# Remove records where doctors attended exceed doctors available
doctor_df = doctor_df[
    doctor_df["Doctors Attended"] <= doctor_df["Doctors Available"]
]

print(
    "Doctor_Data after cleaning:",
    doctor_df.shape
)


# ------------------------------------------------------------
# FACILITY MASTER
# ------------------------------------------------------------

# Facility_Master has no duplicate records,
# so no row removal is required.

print(
    "Facility_Master after checking:",
    facility_df.shape
)

# ================================================================
# FIX FACILITY NAME TYPO IN HOSPITAL DATA
# ================================================================

hospital_df.loc[
    (hospital_df["District"] == "Coimbatore")
    & (hospital_df["Facility Name"] == "Chennai Urban PHC 1"),
    "Facility Name"
] = "Coimbatore Urban PHC 1"

# Recreate Facility_Key after correcting the facility name
hospital_df["Facility_Key"] = (
    hospital_df["District"].astype(str).str.strip()
    + "|"
    + hospital_df["Facility Name"].astype(str).str.strip()
)

# ============================================================
# SAVE FINAL CLEANED WORKBOOK
# ============================================================

cleaned_file_path = (
    project_path / "output" / "TN_Healthcare_Dashboard_Cleaned.xlsx"
)

with pd.ExcelWriter(cleaned_file_path, engine="openpyxl") as writer:

    disease_df.to_excel(
        writer,
        sheet_name="Disease_Data",
        index=False
    )

    emergency_df.to_excel(
        writer,
        sheet_name="Emergency_Data",
        index=False
    )

    hospital_df.to_excel(
        writer,
        sheet_name="Hospital_Data",
        index=False
    )

    doctor_df.to_excel(
        writer,
        sheet_name="Doctor_Data",
        index=False
    )

    facility_df.to_excel(
        writer,
        sheet_name="Facility_Master",
        index=False
    )

print("\n" + "=" * 60)
print("FINAL CLEANED WORKBOOK SAVED")
print("=" * 60)
print(cleaned_file_path)

# ============================================================
# FINAL FACILITY KEY CHECK
# ============================================================

print("\n" + "=" * 60)
print("FINAL FACILITY KEY CHECK")
print("=" * 60)

duplicate_facilities = facility_df[
    facility_df["Facility Name"].duplicated(keep=False)
]

print("Duplicate Facility Names:", len(duplicate_facilities))

if len(duplicate_facilities) > 0:
    print(duplicate_facilities)
else:
    print("Facility Name is unique in Facility_Master.")

    # ============================================================
# CREATE UNIQUE FACILITY KEY
# ============================================================

print("\n" + "=" * 60)
print("CREATING FACILITY KEY")
print("=" * 60)


# Create a unique key using District + Facility Name

disease_df["Facility_Key"] = (
    disease_df["District"].astype(str).str.strip()
    + "|"
    + disease_df["Facility Name"].astype(str).str.strip()
)

emergency_df["Facility_Key"] = (
    emergency_df["District"].astype(str).str.strip()
    + "|"
    + emergency_df["Facility Name"].astype(str).str.strip()
)

hospital_df["Facility_Key"] = (
    hospital_df["District"].astype(str).str.strip()
    + "|"
    + hospital_df["Facility Name"].astype(str).str.strip()
)

doctor_df["Facility_Key"] = (
    doctor_df["District"].astype(str).str.strip()
    + "|"
    + doctor_df["Facility Name"].astype(str).str.strip()
)

facility_df["Facility_Key"] = (
    facility_df["District"].astype(str).str.strip()
    + "|"
    + facility_df["Facility Name"].astype(str).str.strip()
)


# Check whether Facility_Master now has unique keys

duplicate_keys = facility_df[
    facility_df["Facility_Key"].duplicated(keep=False)
]

print(
    "Duplicate Facility Keys:",
    len(duplicate_keys)
)

if len(duplicate_keys) == 0:
    print("Facility_Key is unique in Facility_Master.")
else:
    print(duplicate_keys)


    # ============================================================
# CHECK OPERATIONAL FACILITY KEYS
# ============================================================

print("\n--- OPERATIONAL FACILITY KEY CHECK ---")

# Recreate Facility_Key after all facility name corrections
for df in [
    disease_df,
    emergency_df,
    hospital_df,
    doctor_df,
    facility_df
]:
    df["Facility_Key"] = (
        df["District"].astype(str).str.strip()
        + "|"
        + df["Facility Name"].astype(str).str.strip()
    )

master_keys = set(facility_df["Facility_Key"])

for name, df in [
    ("Disease_Data", disease_df),
    ("Emergency_Data", emergency_df),
    ("Hospital_Data", hospital_df),
    ("Doctor_Data", doctor_df)
]:

    missing_keys = set(df["Facility_Key"]) - master_keys

    print(
        name,
        "keys missing from Facility_Master:",
        len(missing_keys)
    )

    # ============================================================
# INVESTIGATE FACILITY KEY DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATING FACILITY KEY DUPLICATES")
print("=" * 60)

duplicate_key_rows = facility_df[
    facility_df["Facility_Key"].duplicated(keep=False)
].sort_values("Facility_Key")

print("\nDuplicate Facility Keys:")
print(duplicate_key_rows)

print("\nNumber of unique duplicate keys:")
print(duplicate_key_rows["Facility_Key"].nunique())


# ============================================================
# INVESTIGATE MISSING HOSPITAL KEY
# ============================================================

print("\n" + "=" * 60)
print("INVESTIGATING MISSING HOSPITAL KEY")
print("=" * 60)

master_keys = set(facility_df["Facility_Key"])

missing_hospital_keys = set(hospital_df["Facility_Key"]) - master_keys

print("Missing Hospital Keys:")
print(missing_hospital_keys)

for key in missing_hospital_keys:
    print("\nHospital record:")
    print(
        hospital_df[
            hospital_df["Facility_Key"] == key
        ]
    )


    # ============================================================
# FINAL FACILITY CONSISTENCY CHECK
# ============================================================

print("\n" + "=" * 60)
print("FACILITY CONSISTENCY CHECK")
print("=" * 60)


# ------------------------------------------------------------
# 1. Check whether duplicate Facility Keys have
#    different facility attributes
# ------------------------------------------------------------

duplicate_keys = (
    facility_df[
        facility_df["Facility_Key"].duplicated(keep=False)
    ]
    ["Facility_Key"]
    .unique()
)

print("\nNumber of duplicate facility keys:", len(duplicate_keys))


# Check whether each duplicated key has different attributes
facility_variation = (
    facility_df[
        facility_df["Facility_Key"].isin(duplicate_keys)
    ]
    .groupby("Facility_Key")
    .agg(
        Facility_Types=("Facility Type", "nunique"),
        Healthcare_Levels=("Healthcare Level", "nunique"),
        Bed_Strengths=("Bed Strength", "nunique"),
        Doctors_Available=("Doctors Available", "nunique")
    )
    .reset_index()
)

print("\nDuplicate keys with varying attributes:")
print(
    facility_variation[
        (facility_variation["Facility_Types"] > 1)
        | (facility_variation["Healthcare_Levels"] > 1)
        | (facility_variation["Bed_Strengths"] > 1)
        | (facility_variation["Doctors_Available"] > 1)
    ]
)


# ------------------------------------------------------------
# 2. Investigate the Coimbatore facility mismatch
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CHECKING COIMBATORE FACILITY")
print("=" * 60)

facility_name = "Coimbatore Urban PHC 1"

for name, df in [
    ("Disease_Data", disease_df),
    ("Emergency_Data", emergency_df),
    ("Hospital_Data", hospital_df),
    ("Doctor_Data", doctor_df),
    ("Facility_Master", facility_df)
]:

    result = df[
        (df["District"] == "Coimbatore")
        &
        (df["Facility Name"].str.contains(
            "Urban PHC 1",
            case=False,
            na=False
        ))
    ]

    print("\n", name)
    print(result[["District", "Facility Name"]].drop_duplicates())