import os
import csv
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from typing import Dict, List
import redis
import jwt

class ToolManager:
    def __init__(self):
        self.tools_config = {}
        self.deployed_tools = {}
        self.redis_client = redis.Redis(
            host='adlsacreddanielcurilindiumpohl-redis-1',
            port=6379,
            decode_responses=True
        )
        self.parquet_path = "tool_registry.parquet"
        
    def load_csv_tools(self, csv_path: str) -> List[Dict]:
        """Lädt Tools aus einer CSV-Datei"""
        tools = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tool = {
                    "name": row.get("name", ""),
                    "type": row.get("type", ""),
                    "description": row.get("description", ""),
                    "access_level": row.get("access_level", "public"),
                    "config": {
                        "memory_limit": "512M",
                        "cpu_limit": "0.5",
                        "network": "tool-network",
                        "volumes": [],
                        "environment": {}
                    }
                }
                tools.append(tool)
        return tools
    
    def load_excel_tools(self, excel_path: str) -> List[Dict]:
        """Lädt Tools aus einer Excel-Datei"""
        df = pd.read_excel(excel_path)
        tools = []
        for _, row in df.iterrows():
            tool = {
                "name": row.get("name", ""),
                "type": row.get("type", ""),
                "description": row.get("description", ""),
                "access_level": row.get("access_level", "public"),
                "config": {
                    "memory_limit": "512M",
                    "cpu_limit": "0.5",
                    "network": "tool-network",
                    "volumes": [],
                    "environment": {}
                }
            }
            tools.append(tool)
        return tools
    
    def process_tools_directory(self, directory: str) -> None:
        """Verarbeitet einen Ordner mit Tool-Definitionen"""
        path = Path(directory)
        for file in path.glob("**/*"):
            if file.suffix.lower() in ['.csv']:
                tools = self.load_csv_tools(str(file))
                self.tools_config[file.stem] = tools
            elif file.suffix.lower() in ['.xlsx', '.xls']:
                tools = self.load_excel_tools(str(file))
                self.tools_config[file.stem] = tools
    
    def deploy_tool(self, tool_config: Dict) -> str:
        """Deployed ein einzelnes Tool"""
        # Nutzt das deploy_tool.py Script im Hintergrund
        tool_id = hashlib.sha256(tool_config["name"].encode()).hexdigest()[:12]
        
        # Speichere Deployment-Informationen
        self.deployed_tools[tool_id] = {
            "config": tool_config,
            "status": "deployed",
            "access_url": f"/tools/{tool_id}"
        }
        
        return tool_id
    
    def get_tool_access_url(self, tool_id: str) -> str:
        """Generiert eine sichere Zugriffs-URL für ein Tool"""
        if tool_id in self.deployed_tools:
            tool = self.deployed_tools[tool_id]
            if tool["config"]["access_level"] == "private":
                return f"/auth/tools/{tool_id}?token={{jwt_token}}"
            return f"/tools/{tool_id}"
        return ""
    
    def save_state(self) -> None:
        """Speichert den aktuellen Zustand"""
        state = {
            "tools_config": self.tools_config,
            "deployed_tools": self.deployed_tools
        }
        with open("tool_manager_state.json", "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self) -> None:
        """Lädt den gespeicherten Zustand"""
        if os.path.exists("tool_manager_state.json"):
            with open("tool_manager_state.json", "r") as f:
                state = json.load(f)
                self.tools_config = state.get("tools_config", {})
                self.deployed_tools = state.get("deployed_tools", {})
    
    def register_tool(self, tool_id: str, tool_info: Dict) -> bool:
        """Registriert ein Tool in Redis und Parquet"""
        try:
            # Redis Speicherung
            self.redis_client.hset(f"tool:{tool_id}", mapping=tool_info)
            
            # Parquet Speicherung
            if os.path.exists(self.parquet_path):
                existing_df = pd.read_parquet(self.parquet_path)
            else:
                existing_df = pd.DataFrame()
                
            new_df = pd.DataFrame([{
                'tool_id': tool_id,
                **tool_info
            }])
            
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_parquet(self.parquet_path, index=False)
            
            return True
        except Exception as e:
            print(f"Fehler bei der Tool-Registrierung: {e}")
            return False
    
    def get_tool(self, tool_id: str) -> Dict:
        """Liest Tool-Informationen aus Redis"""
        return self.redis_client.hgetall(f"tool:{tool_id}")
    
    def list_tools(self) -> List[Dict]:
        """Listet alle registrierten Tools auf"""
        tool_keys = self.redis_client.keys('tool:*')
        tools = []
        for key in tool_keys:
            tool_info = self.redis_client.hgetall(key)
            tools.append(tool_info)
        return tools
    
    def export_tools_parquet(self) -> str:
        """Exportiert alle Tools als Parquet-Datei"""
        tools = self.list_tools()
        df = pd.DataFrame(tools)
        df.to_parquet(self.parquet_path, index=False)
        return self.parquet_path
    
    def import_tools_parquet(self, file_path: str) -> bool:
        """Importiert Tools aus einer Parquet-Datei"""
        try:
            df = pd.read_parquet(file_path)
            for _, row in df.iterrows():
                tool_info = row.to_dict()
                tool_id = tool_info.pop('tool_id')
                self.register_tool(tool_id, tool_info)
            return True
        except Exception as e:
            print(f"Fehler beim Import: {e}")
            return False