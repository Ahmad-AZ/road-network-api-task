# Road Network API (FastAPI)

---

## Description

A simple REST API for managing road networks with version control, using **FastAPI**, **PostgreSQL**, and **PostGIS**.

---

## Features

1. Upload GeoJSON road networks for different customers.
2. Update networks by adding new edges (old edges marked outdated).
3. Retrieve network edges in GeoJSON format (with timestamp filter).

---

## Project Structure


.
├── app/
│   ├── main.py           → FastAPI entry point
│   ├── models.py         → SQLAlchemy models with geometry support
│   ├── database.py       → DB connection (PostgreSQL + PostGIS)
│   ├── schemas.py        → Pydantic models (optional)
│   └── routers/
│       └── networks.py   → All API routes
├── requirements.txt      → Python dependencies
├── Dockerfile            → Builds the FastAPI app
├── docker-compose.yml    → Runs FastAPI + PostGIS together
└── README.md

---

## Usage

1. **Run the project**

    ```bash
    $ docker-compose up --build
    ```

2. **Upload a network**

    `POST /networks/upload`
    `form-data: file (.geojson), name, customer_id`

3. **Update a network**

    `POST /networks/update`
    `form-data: file (.geojson), network_name, customer_id`

4. **Get edges of a network**

    `GET /networks/{network_id}/edges?customer_id=...&timestamp=...`

---

## Requirements

* Python 3.12+
* Docker & Docker Compose
* PostGIS-enabled PostgreSQL (handled in docker-compose)

---

## Notes

* All geometries are stored as **LINESTRING** (WKT format).
* Timestamp must be in **ISO 8601** (e.g., `2025-07-22T14:00:00`).
* GeoJSON responses are compliant with standard format.