#!/bin/bash

echo "🚀 Starting Dynamic Internal Talent Mapper..."

echo "📌 Step 1: Build vector DB"
python3 scripts/build_vector_db.py

echo "📌 Step 2: Start Streamlit UI"
streamlit run ui/app.py --server.port=8501 --server.address=0.0.0.0
