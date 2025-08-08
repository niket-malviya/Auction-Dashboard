import pandas as pd
import uuid
from werkzeug.security import generate_password_hash
from models.player import Player
from models.tournament import Tournament
from app.extensions import db
from io import BytesIO
import logging

class ExcelImportService:
    def __init__(self):
        self.required_columns = [
            'name', 'last_name', 'flat_no', 'age', 'mobile_number', 
            'bowler_type', 'batter_type', 'category'
        ]
        self.optional_columns = ['img_url']
        
    def validate_excel_file(self, file):
        """Validate the uploaded Excel file"""
        try:
            # Check file extension
            if not file.filename.lower().endswith(('.xlsx', '.xls')):
                return False, "File must be an Excel file (.xlsx or .xls)"
            
            # Read the Excel file
            df = pd.read_excel(file)
            
            # Check if required columns exist
            missing_columns = []
            for col in self.required_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"
            
            # Check if file is empty
            if df.empty:
                return False, "Excel file is empty"
            
            return True, "File is valid"
            
        except Exception as e:
            return False, f"Error reading Excel file: {str(e)}"
    
    def validate_player_data(self, row, row_number):
        """Validate individual player data row"""
        errors = []
        
        # Required field validations
        if pd.isna(row.get('name')) or str(row['name']).strip() == '':
            errors.append("Name is required")
        
        if pd.isna(row.get('last_name')) or str(row['last_name']).strip() == '':
            errors.append("Last name is required")
        
        if pd.isna(row.get('flat_no')) or str(row['flat_no']).strip() == '':
            errors.append("Flat number is required")
        
        # Age validation
        try:
            age = int(row.get('age', 0))
            if age <= 0 or age > 100:
                errors.append("Age must be between 1 and 100")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number")
        
        # Mobile number validation
        mobile = str(row.get('mobile_number', '')).strip()
        if not mobile or len(mobile) < 10:
            errors.append("Valid mobile number is required")
        
        # Bowler type validation
        bowler_type = str(row.get('bowler_type', '')).strip().lower()
        if bowler_type and bowler_type not in ['left', 'right']:
            errors.append("Bowler type must be 'left' or 'right'")
        
        # Batter type validation
        batter_type = str(row.get('batter_type', '')).strip().lower()
        if batter_type and batter_type not in ['left', 'right']:
            errors.append("Batter type must be 'left' or 'right'")
        
        # Category validation
        category = str(row.get('category', '')).strip().lower()
        if category not in ['gold', 'silver', 'bronze']:
            errors.append("Category must be 'gold', 'silver', or 'bronze'")
        
        return errors
    
    def import_players_from_excel(self, file, tournament_id):
        """Import players from Excel file"""
        try:
            # Validate tournament exists
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return False, "Tournament not found", []
            
            # Validate Excel file
            is_valid, message = self.validate_excel_file(file)
            if not is_valid:
                return False, message, []
            
            # Read Excel file
            df = pd.read_excel(file)
            
            # Process each row
            imported_players = []
            errors = []
            skipped_rows = []
            
            for index, row in df.iterrows():
                row_number = index + 2  # Excel rows start from 2 (1 is header)
                
                # Validate row data
                row_errors = self.validate_player_data(row, row_number)
                
                if row_errors:
                    errors.append({
                        'row': row_number,
                        'errors': row_errors,
                        'data': row.to_dict()
                    })
                    continue
                
                # Check if player already exists (by flat_no and tournament)
                existing_player = Player.query.filter_by(
                    flat_no=str(row['flat_no']).strip(),
                    tournament_id=tournament_id
                ).first()
                
                if existing_player:
                    skipped_rows.append({
                        'row': row_number,
                        'reason': f"Player with flat number {row['flat_no']} already exists",
                        'data': row.to_dict()
                    })
                    continue
                
                # Create new player
                try:
                    new_player = Player(
                        id=uuid.uuid4(),
                        name=str(row['name']).strip(),
                        last_name=str(row['last_name']).strip(),
                        flat_no=str(row['flat_no']).strip(),
                        age=int(row['age']),
                        mobile_number=str(row['mobile_number']).strip(),
                        bowler_type=str(row['bowler_type']).strip().lower() if pd.notna(row.get('bowler_type')) else None,
                        batter_type=str(row['batter_type']).strip().lower() if pd.notna(row.get('batter_type')) else None,
                        category=str(row['category']).strip().lower(),
                        img_url=str(row['img_url']).strip() if pd.notna(row.get('img_url')) else None,
                        tournament_id=tournament_id
                    )
                    
                    db.session.add(new_player)
                    imported_players.append({
                        'id': str(new_player.id),
                        'name': new_player.name,
                        'last_name': new_player.last_name,
                        'flat_no': new_player.flat_no,
                        'age': new_player.age,
                        'category': new_player.category
                    })
                    
                except Exception as e:
                    errors.append({
                        'row': row_number,
                        'errors': [f"Error creating player: {str(e)}"],
                        'data': row.to_dict()
                    })
            
            # Commit all changes if no errors
            if not errors:
                db.session.commit()
                return True, f"Successfully imported {len(imported_players)} players", {
                    'imported': imported_players,
                    'skipped': skipped_rows,
                    'errors': errors
                }
            else:
                # Rollback if there are errors
                db.session.rollback()
                return False, f"Import failed with {len(errors)} errors", {
                    'imported': [],
                    'skipped': skipped_rows,
                    'errors': errors
                }
                
        except Exception as e:
            db.session.rollback()
            logging.error(f"Excel import error: {str(e)}")
            return False, f"Import failed: {str(e)}", []
    
    def get_excel_template(self):
        """Generate Excel template for player import"""
        try:
            # Create sample data
            sample_data = {
                'name': ['John', 'Jane', 'Mike'],
                'last_name': ['Doe', 'Smith', 'Johnson'],
                'flat_no': ['101', '102', '103'],
                'age': [25, 28, 30],
                'mobile_number': ['1234567890', '0987654321', '1122334455'],
                'bowler_type': ['right', 'left', 'right'],
                'batter_type': ['left', 'right', 'left'],
                'category': ['silver', 'gold', 'bronze'],
                'img_url': ['', '', '']
            }
            
            df = pd.DataFrame(sample_data)
            
            # Create Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Players', index=False)
                
                # Get the workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Players']
                
                # Add instructions
                instructions = [
                    ['INSTRUCTIONS:'],
                    ['1. Fill in all required fields (name, last_name, flat_no, age, mobile_number, bowler_type, batter_type, category)'],
                    ['2. Optional fields: img_url'],
                    ['3. bowler_type and batter_type must be "left" or "right"'],
                                         ['4. category must be "gold", "silver", or "bronze"'],
                    ['5. age must be a number between 1 and 100'],
                    ['6. mobile_number must be at least 10 digits'],
                    ['7. flat_no must be unique for each player'],
                    [''],
                    ['SAMPLE DATA:']
                ]
                
                for i, instruction in enumerate(instructions):
                    worksheet.cell(row=i+1, column=1, value=instruction[0])
                
                # Move sample data down
                for i, row in enumerate(df.values):
                    for j, value in enumerate(row):
                        worksheet.cell(row=i+len(instructions)+1, column=j+1, value=value)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logging.error(f"Template generation error: {str(e)}")
            return None 