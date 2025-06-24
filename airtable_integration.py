
import os
import requests
import time
import threading
from datetime import datetime, timedelta
import re
from main import CodeAnalyzer, clone_repository, get_github_user_info, analyze_commits, should_analyze_file
import tempfile
import shutil
from collections import defaultdict

class AirtableIntegration:
    def __init__(self):
        self.api_key = os.environ.get("AIRTABLE_API_KEY")
        self.base_url = "https://api.airtable.com/v0"
        self.analyzer = CodeAnalyzer()
        
        # Configuration for each table
        self.tables_config = {
            "Toppings": {
                "base_id": "appwzSybRkGKmv1vU",
                "table_name": "Submission Review"
            },
            "Waffles": {
                "base_id": "app7WAAuSzpy8miWt",
                "table_name": "Submission Review"
            },
            "Club Grants": {
                "base_id": "appSnnIu0BhjI3E1p",
                "table_name": "YSWS Project Submission"
            },
            "Swirl": {
                "base_id": "app65NU0LhsflmT0P",
                "table_name": "Submission Review"
            },
            "Boba": {
                "base_id": "app05mIKwNPO2l1vT",
                "table_name": "Websites",
                "alt_table": "YSWS Project Submission"
            }
        }
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Track processed records to avoid duplicates
        self.processed_records = set()
        
    def get_records(self, base_id, table_name, filter_formula=None):
        """Get records from Airtable"""
        url = f"{self.base_url}/{base_id}/{table_name}"
        params = {}
        
        if filter_formula:
            params['filterByFormula'] = filter_formula
            
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json().get('records', [])
            else:
                print(f"❌ Error fetching records from {table_name}: {response.status_code} {response.text}")
                return []
        except Exception as e:
            print(f"❌ Exception fetching records: {e}")
            return []
    
    def update_record(self, base_id, table_name, record_id, fields):
        """Update a record in Airtable"""
        url = f"{self.base_url}/{base_id}/{table_name}/{record_id}"
        data = {"fields": fields}
        
        try:
            response = requests.patch(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"✅ Updated record {record_id} in {table_name}")
                return True
            else:
                print(f"❌ Error updating record {record_id}: {response.status_code} {response.text}")
                return False
        except Exception as e:
            print(f"❌ Exception updating record: {e}")
            return False
    
    def extract_github_url(self, text):
        """Extract GitHub URL from text"""
        if not text:
            return None
            
        # Look for GitHub URLs
        github_patterns = [
            r'https://github\.com/[^\s\)]+',
            r'http://github\.com/[^\s\)]+',
            r'github\.com/[^\s\)]+',
        ]
        
        for pattern in github_patterns:
            match = re.search(pattern, str(text))
            if match:
                url = match.group(0)
                # Ensure it starts with https://
                if not url.startswith('http'):
                    url = 'https://' + url
                return url
        
        return None
    
    def analyze_github_repository(self, repo_url):
        """Analyze GitHub repository and return AI probability"""
        if not repo_url:
            return None
            
        print(f"🔍 Analyzing repository: {repo_url}")
        
        temp_dir = None
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            
            # Clone repository
            repo = clone_repository(repo_url, temp_dir)
            
            # Get user info
            user_info = get_github_user_info(repo_url)
            
            # Analyze commits
            commits = analyze_commits(repo)
            
            # Analyze code files
            total_files = 0
            total_comments = 0
            total_code_lines = 0
            total_ai_score = 0
            file_contents = []
            
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, temp_dir)
                    
                    if should_analyze_file(rel_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            
                            result = self.analyzer.analyze_file(rel_path, content)
                            
                            # File metadata analysis
                            metadata_score = self.analyzer.analyze_file_metadata(rel_path, content)
                            result['ai_score'] += metadata_score
                            result['ai_score'] = min(result['ai_score'], 100)
                            
                            total_files += 1
                            total_comments += result['comments']
                            total_code_lines += result['code_lines']
                            total_ai_score += result['ai_score']
                            file_contents.append(content)
                            
                        except:
                            continue
            
            # Analyze commit patterns
            commit_pattern_score = self.analyzer.analyze_commit_patterns(commits)
            total_ai_score += commit_pattern_score
            
            # Detect code duplication
            duplication_score = self.analyzer.detect_code_duplication(file_contents)
            total_ai_score += duplication_score
            
            # Calculate overall metrics
            if total_files > 0:
                avg_ai_score = total_ai_score / total_files
                overall_likelihood = self.analyzer.get_ai_likelihood(avg_ai_score)
            else:
                avg_ai_score = 0
                overall_likelihood = "Not AI"
            
            # Map to Airtable values
            if overall_likelihood == "Not AI":
                return "Pass"
            elif overall_likelihood == "Maybe AI":
                return "Potential AI"
            else:  # "Probly AI" or "Definitly AI"
                return "Definitely AI"
                
        except Exception as e:
            print(f"❌ Error analyzing repository {repo_url}: {e}")
            return None
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def process_table(self, project_name, config):
        """Process a single table for new records"""
        base_id = config["base_id"]
        table_name = config["table_name"]
        
        print(f"🔍 Checking {project_name} - {table_name}")
        
        # Filter for records that don't have AI Probability set or are empty
        filter_formula = "OR({AI Probability} = '', {AI Probability} = BLANK())"
        
        records = self.get_records(base_id, table_name, filter_formula)
        
        # Also check alternative table for Boba if specified
        if "alt_table" in config:
            alt_records = self.get_records(base_id, config["alt_table"], filter_formula)
            records.extend(alt_records)
        
        for record in records:
            record_id = record['id']
            fields = record.get('fields', {})
            
            # Skip if already processed
            unique_key = f"{base_id}_{table_name}_{record_id}"
            if unique_key in self.processed_records:
                continue
            
            # Look for GitHub URL in various possible fields
            github_url = None
            url_fields = ['Code URL', 'Repository URL', 'GitHub URL', 'Project URL', 'URL', 'Code', 'Repository']
            
            for field_name in url_fields:
                if field_name in fields:
                    github_url = self.extract_github_url(fields[field_name])
                    if github_url:
                        break
            
            # If no direct URL field, check description or other text fields
            if not github_url:
                text_fields = ['Description', 'Project Description', 'Notes', 'Details']
                for field_name in text_fields:
                    if field_name in fields:
                        github_url = self.extract_github_url(fields[field_name])
                        if github_url:
                            break
            
            if github_url:
                print(f"📍 Found GitHub URL in {project_name}: {github_url}")
                
                # Analyze the repository
                ai_probability = self.analyze_github_repository(github_url)
                
                if ai_probability:
                    # Update the record
                    update_fields = {"AI Probability": ai_probability}
                    
                    table_to_update = table_name
                    if "alt_table" in config and record.get('fields', {}).get('Table') == config["alt_table"]:
                        table_to_update = config["alt_table"]
                    
                    success = self.update_record(base_id, table_to_update, record_id, update_fields)
                    
                    if success:
                        print(f"✅ {project_name}: Set AI Probability to '{ai_probability}' for record {record_id}")
                        self.processed_records.add(unique_key)
                    else:
                        print(f"❌ Failed to update {project_name} record {record_id}")
                else:
                    print(f"⚠️ Could not analyze repository: {github_url}")
            else:
                print(f"⚠️ No GitHub URL found in {project_name} record {record_id}")
    
    def monitor_tables(self):
        """Monitor all tables for new records"""
        print("🚔 Officer Heidi Airtable monitoring started!")
        
        while True:
            try:
                print(f"\n🔄 Starting monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                for project_name, config in self.tables_config.items():
                    try:
                        self.process_table(project_name, config)
                    except Exception as e:
                        print(f"❌ Error processing {project_name}: {e}")
                
                print(f"✅ Monitoring cycle completed. Sleeping for 5 minutes...")
                time.sleep(300)  # Check every 5 minutes
                
            except KeyboardInterrupt:
                print("🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def start_airtable_monitoring():
    """Start Airtable monitoring in a separate thread"""
    integration = AirtableIntegration()
    monitor_thread = threading.Thread(target=integration.monitor_tables, daemon=True)
    monitor_thread.start()
    return monitor_thread

if __name__ == "__main__":
    # For testing
    integration = AirtableIntegration()
    integration.monitor_tables()
