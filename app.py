# app.py
"summary": {
"rows": rows,
"cols": cols,
"null_pct": null_pct,
"numeric_cols": int(num_df.shape[1])

"numeric_stats": numeric_stats,
"top_categories": top_categories,





@app.post("/analyze")
async def analyze(api_key: str = Form(...), file: UploadFile = File(...)):
check_and_increment_usage(api_key)
if not file.filename.lower().endswith('.csv'):
raise HTTPException(status_code=400, detail="Envie um arquivo .csv")


content = await file.read()
try:
df = pd.read_csv(io.BytesIO(content))
except Exception:
# tenta ; como separador (comum no BR)
try:
df = pd.read_csv(io.BytesIO(content), sep=';')
except Exception as e:
raise HTTPException(status_code=400, detail=f"CSV inválido: {e}")


result = analyze_dataframe(df)
return result




# --- Utilitário (admin) para criar chaves ---
@app.post("/admin/create-key")
async def create_key(secret: str = Form(...), key: str = Form(...), plan: str = Form("pro"), daily_limit: int = Form(50)):
if secret != os.environ.get("ADMIN_SECRET", "changeme"):
raise HTTPException(status_code=403, detail="Não autorizado")
with sqlite3.connect(DB_PATH) as conn:
c = conn.cursor()
c.execute("INSERT OR REPLACE INTO api_keys(key, plan, daily_limit) VALUES (?, ?, ?)", (key, plan, daily_limit))
conn.commit()
return {"status": "ok", "key": key, "plan": plan, "daily_limit": daily_limit}




if __name__ == "__main__":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=PORT)
