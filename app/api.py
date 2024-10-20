# api.py (updated)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rules import create_rule, evaluate_rule, combine_rules
from database import MongoDB
import json

app = FastAPI()

# Initialize MongoDB connection
mongodb = MongoDB(uri="mongodb://localhost:27017/", db_name="rule_engine_db")

class RuleInput(BaseModel):
    rule_string: str

class EvaluationInput(BaseModel):
    rule_id: str
    user_data: dict

@app.post("/create-rule/")
def create_rule_endpoint(rule: RuleInput):
    try:
        ast = create_rule(rule.rule_string)
        ast_json = json.loads(ast.__dict__)  # Convert AST to JSON-serializable format
        rule_id = mongodb.insert_rule(rule.rule_string, ast_json)
        return {"rule_id": rule_id, "ast": repr(ast)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate-rule/")
def evaluate_rule_endpoint(data: EvaluationInput):
    try:
        rule_doc = mongodb.get_rule(data.rule_id)
        if not rule_doc:
            raise HTTPException(status_code=404, detail="Rule not found")
        ast = rule_doc['ast']
        result = evaluate_rule(ast, data.user_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/update-rule/{rule_id}")
def update_rule(rule_id: str, rule: RuleInput):
    try:
        ast = create_rule(rule.rule_string)
        ast_json = json.loads(ast.__dict__)
        mongodb.update_rule(rule_id, rule.rule_string, ast_json)
        return {"message": "Rule updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete-rule/{rule_id}")
def delete_rule(rule_id: str):
    try:
        mongodb.delete_rule(rule_id)
        return {"message": "Rule deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the FastAPI server
# uvicorn api:app --reload
