# Self-Service Database API Documentation

---
Author: [Tiger Nie] <nhl0819@gmail.com>

Github: <https://github.com/haolinnie/Self-Service-Database-Server>

Documentation: <https://github.com/haolinnie/Self-Service-Database-Server/blob/master/ssd_api/APIDocumentation.md>

Testing url: <https://tigernie.com/ssd_api>

---

## API Endpoints

### Get list of table names

Get the names of all the tables in the database.

URL: `baseURL/ssd_api/get_table`

Type: `GET`

Example:

`https://tigernie.com/ssd_api/get_table`

Returns:

```json
{
    "table_names": [
        "pt_deid",
        "diagnosis_deid",
        "lab_value_deid",
        "medication_deid",
        "medication_administration_deid",
        "smart_data_deid",
        "visit_movement_deid",
        "image_procedure",
        "exam_deid",
        "image_deid"
    ]
}
```

---

### Get columns in a table

Given a **table_name**, return the columns of the table.

URL: `baseURL/ssd_api/get_table_cols`

Type: `GET`

Example: To get the column names of **pt_deid**

`https://tigernie.com/ssd_api/get_table_cols?table_name=pt_deid`

Returns:

```json
{
    "table_name": "pt_deid",
    "columns": [
        "index",
        "pt_id",
        "dob",
        "over_90",
        "ethnicity"
    ]
}
```

---

### Get distinct values in a table column

Given a **table_name** and **col_name**, return the unique values in that column.
Can be used to obtain unique values from a column (e.g. medication) to
populate a multiple choice filter.

URL: `baseURL/ssd_api/get_distinct`

Type: `GET`

Example 1: To get the distinct values in table **pt_deid** column **pt_id**

`https://tigernie.com/ssd_api/get_distinct?table_name=pt_deid&col_name=pt_id`

Returns:

```json
{
    "data": [
        20676,
        36440,
        50765,
        53754,
        59153,
        64153,
        64656,
        66166,
        66172,
        66475
    ],
    "table_name": "pt_deid",
    "col_name": "pt_id"
}
```

Example 2: To get a **special** category ('eye_diagnosis' and 'systemic_diagnosis')

`https://tigernie.com/ssd_api/get_distinct?special=eye_diagnosis`

Returns:

```json
{
    "col_name": "eye_diagnosis",
    "data": [
        "Arterial branch occlusion of retina",
        "Branch retinal vein occlusion with macular edema (disorder)",
        "Central retinal vein occlusion (disorder)",
        "Central vein occlusion of retina",
        "Chronic iridocyclitis, bilateral",
        "Chronic iridocyclitis, unspecified",
        "Cystoid macular degeneration of retina",
        "Cystoid macular degeneration, bilateral",
        "Degenerative disorder of macula (disorder)",
        "Iridocyclitis (disorder)",
        "Myopia (disorder)",
        "Retinal edema",
        "Retinal hemorrhage (finding)",
        "Retinal neovascularization NOS",
        "Retinal vasculitis",
        "Retinal vasculitis (disorder)",
        "Retinal vasculitis, bilateral",
        "Retinal vasculitis, unspecified eye",
        "Tributary (branch) retinal vein occlusion, bilateral, with macular edema",
        "Unspecified chorioretinal inflammation, left eye"
    ],
    "table_name": null
}
```

---

### Filter a table for specific pt_id

Given a list of **pt_id** and a **table_name**, return row data for
those patients. Note that there can be an arbitrary number of pt_id values,
just chain them like so `pt_id=<int>&pt_id=<int>&..`.

URL: `baseURL/ssd_api/filter_table_with_ptid?pt_id=<int>&table_name=<string>`

Type: `GET`

Example: Retrieve data for patients **[20676, 36440]** from table **diagnosis_deid**

`https://tigernie.com/ssd_api/filter_table_with_ptid?pt_id=20676&pt_id=36440&pt_id=50765&table_name=diagnosis_deid`

Returns (truncated):

```json
{
    "columns": [
        "index",
        "diagnosis_id",
        "pt_id",
        "diagnosis_code",
        "diagnosis_code_set",
        "diagnosis_start_dt",
        "diagnosis_end_dt",
        "diagnosis_name"
    ],
    "data": [
        [
            80,
            22198049,
            20676,
            "V58.83",
            "ICD-9-CM",
            "2014-05-02 15:28:00",
            "2100-11-28 00:00:00",
            "ENCOUNTER FOR THERAPEUTIC DRUG MONITORING"
        ],
        [
            81,
            22198050,
            20676,
            "V76.10",
            "ICD-9-CM",
            "2013-12-04 00:00:00",
            null,
            "Breast screening, unspecified"
        ],
        [
            82,
            22198051,
            20676,
            "SNOMED#249366005",
            "SNOMED CT",
            "2018-02-18 00:00:00",
            null,
            "Bleeding from nose (finding)"
        ],
    ]
}
```

---

### Retrieves Patient History

Given a list of **pt_id**, return the `medication[{id, generic_name, therapeutic_class}], eye_diagnosis[{diagnosis, date}], systemic_diagnosis[{diagnosis, date}], lab_values[{lab_name, lab_value, unit, date}], vision[{name, value, smart_data_id, date}], pressure[{name, value, smart_data_id, date}]` for each **pt_id**. This provides all the data to populate the Patient History table. All listed items are sorted by date.

URL: `baseURL/ssd_api/patients`

Type: `GET`

Example: Retrieve patient history for patients **[20676, 36440]**

`https://tigernie.com/ssd_api/patients?pt_id=20676&pt_id=36440`

Returns (truncated):

```json
{
    "20676": {
        "medication": [
            {"date": "2010-12-03 16:19:00", "generic_name": "Spacer/Aerosol-Holding Chambers - Device", "id": 12435512, "therapeutic_class": "Miscellaneous Products"},
            {"date": "2013-12-08 09:02:00", "generic_name": "Fluticasone Propionate Nasal Susp 50 MCG/ACT", "id": 12435513, "therapeutic_class": "Respiratory Agents"},
            {"date": "2015-03-19 09:31:00", "generic_name": "Apremilast Tab 30 MG", "id": 12435510, "therapeutic_class": "Analgesics & Anesthetics"},
        ],
        "eye_diagnosis": [],
        "systemic_diagnosis": [
            {"diagnosis": "Breast screening, unspecified", "date": "2013-12-04 00:00:00"},
            {"diagnosis": "Breast neoplasm screening status (finding)", "date": "2013-12-04 00:00:00"},
            {"diagnosis": "ENCOUNTER FOR THERAPEUTIC DRUG MONITORING", "date": "2014-05-02 15:28:00"}
        ],
        "lab_values": [
            {"lab_name": "FEMORAL NECK(RIGHT): Z-SCORE", "lab_value": "-0.4", "unit": "None", "date": "2010-06-26 20:38:00"},
            {"lab_name": "TOTAL HIP BILATERAL AVERAGE: BMD", "lab_value": "0.934", "unit": "g/cm2", "date": "2010-06-26 20:38:00"},
            {"lab_name": "TOTAL HIP(RIGHT): Z-SCORE", "lab_value": "-0.5", "unit": "None", "date": "2010-06-26 20:38:00"}
        ],
        "vision": [
            {"name": "FINDINGS - TESTS - EYES - VISUAL ACUITY - VA - METHOD - REFRACTION - MANIFEST REFRACTION - MANIFEST REFRACTION - RIGHT DIST VA", "value": "20/20", "smart_data_id": 23773081, "date": "2014-08-09 00:00:00"}
            {"name": "FINDINGS - TESTS - EYES - VISUAL ACUITY - VA - METHOD - REFRACTION - MANIFEST REFRACTION - MANIFEST REFRACTION - LEFT DIST VA", "value": "20/20-1", "smart_data_id": 23773161, "date": "2014-08-09 00:00:00"}
            {"name": "FINDINGS - TESTS - EYES - VISUAL ACUITY - VA - METHOD - REFRACTION - MANIFEST REFRACTION - MANIFEST REFRACTION - RIGHT DIST VA", "value": "20/20", "smart_data_id": 23768223, "date": "2017-05-03 00:00:00"}
        ],
        "pressure": [
            {"name": "FINDINGS - TESTS - EYES - TONOMETRY - IOP - INTRAOCULAR PRESSURE - LEFT", "value": "14", "smart_data_id": "2014-08-09 00:00:00"},
            {"name": "FINDINGS - TESTS - EYES - TONOMETRY - IOP - INTRAOCULAR PRESSURE - RIGHT", "value": "14", "smart_data_id": "2014-08-09 00:00:00"},
            {"name": "FINDINGS - TESTS - EYES - TONOMETRY - IOP - INTRAOCULAR PRESSURE - LEFT", "value": "14", "smart_data_id": "2017-05-03 00:00:00"}
        ],
        "image_type": [
			"Af",
			"Ir",
			"FA"
		]
}
```

---

### Retrieves Patient Images

Given a list of **pt_id**, return the `exam_id, exam_date, images[]` for each **pt_id**.

URL: `baseURL/ssd_api/patient_images`

Type: `GET`

Example: Retrieve patient images for patients **[20676, 36440]**

`https://tigernie.com/ssd_api/patient_images?pt_id=20676&pt_id=36440`

Returns (truncated):

```json
{
    "20676": [
        {
            "exam_id": 27162,
            "exam_date": "2018-08-09 00:00:00",
            "images": [
                {
                    "image_id": 1313149,
                    "image_num": 0,
                    "image_type": "Image",
                    "image_laterality": "OD",
                    "image_procedure_id": "Af"
                },
                {
                    "image_id": 1313150,
                    "image_num": 0,
                    "image_type": "Image",
                    "image_laterality": "OS",
                    "image_procedure_id": "Ir"
                },
                {
                    "image_id": 1313151,
                    "image_num": 0,
                    "image_type": "Image",
                    "image_laterality": "OS",
                    "image_procedure_id": "Af"
                }
            ]
        }
    ]
}
```

---

### Filter

Given a dictionary of filter parameters, return ....

URL: `baseURL/ssd_api/filter`

Type: `POST`

Input format: Categorical filters (e.g. eye_diagnosis, ethnicity) must be given as a list of strings: `({"eye_diagnosis": ["retinal edema"]})`. Numerical filters (e.g. pressure and vision) must be given as two key value pairs: `({"left_pressure": {"less": 50, "more": 20}, "right_vision": {"less": "20/40"}})`

Example:

`https://tigernie.com/ssd_api/filter`

Input data:

```JSON
{
    "filters": {
        "eye_diagnosis" : ["retinal edema"],
        "systemic_diagnosis": ["gout"],
        "age": {
            "less": 50
        },
        "ethnicity": ["asian"],
        "image_procedure_type": ["IR_OCT"],
        "labs": {"Calcium": 4},
        "medication_generic_name": ["Ketorolac"],
        "medication_therapuetic_name": ["CNS Agent"],
        "left_vision": {
            "less": "20/40"
        },
        "right_vision": {
            "less": "20/40",
            "more": "20/200"
        },
         "left_pressure": {
            "less": 50
        },
        "right_pressure": {
            "equal": 100,
            "between": [120,200]
        }
    }
}
```

Returns (truncated):

```json
{
    "pt_id": [123,123,123]
}
```