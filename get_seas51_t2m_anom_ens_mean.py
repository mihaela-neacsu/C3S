import cdsapi

dataset = "seasonal-postprocessed-single-levels"
request = {
    "originating_centre": "ecmwf",
    "system": "51",
    "variable": ["2m_temperature_anomaly"],
    "product_type": ["ensemble_mean"],
    "year": ["YY"],
    "month": ["MM"],
    "leadtime_month": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ],
    "data_format": "grib",
    "area": [75, -25, 30, 60],
    "grid":  [0.25,0.25]
    }

client = cdsapi.Client()
client.retrieve(dataset, request).download()

