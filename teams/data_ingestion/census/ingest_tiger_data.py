"""
India Tiger Census Data Ingestion Script

This script loads historical tiger census data for India from CSV and JSON files.
Data source: National Tiger Conservation Authority (NTCA)
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any


class TigerCensusDataLoader:
    """Load and process India tiger census data"""
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
    
    def load_national_census(self) -> List[Dict[str, Any]]:
        """Load national-level tiger census data from CSV"""
        csv_file = self.data_dir / "india_tiger_census_national.csv"
        
        data = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                record = {
                    'year': int(row['year']),
                    'population': int(row['population']),
                    'change_from_previous': int(row['change_from_previous']) if row['change_from_previous'] else None,
                    'percent_change': float(row['percent_change']) if row['percent_change'] else None,
                    'data_source': row['data_source'],
                    'survey_method': row['survey_method']
                }
                data.append(record)
        
        return data
    
    def load_state_breakdown(self, year: int = 2022) -> List[Dict[str, Any]]:
        """Load state-level tiger census data from CSV"""
        csv_file = self.data_dir / f"india_tiger_census_states_{year}.csv"
        
        data = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    'state': row['state'],
                    'population': int(row['population']),
                    'percent_of_total': float(row['percent_of_total']),
                    'rank': int(row['rank']),
                    'region': row['region'],
                    'census_year': int(row['census_year'])
                }
                data.append(record)
        
        return data
    
    def load_complete_dataset(self) -> Dict[str, Any]:
        """Load complete tiger census data from JSON"""
        json_file = self.data_dir / "india_tiger_census.json"
        
        with open(json_file, 'r') as f:
            return json.load(f)
    
    def get_latest_population(self) -> int:
        """Get the most recent tiger population count"""
        data = self.load_national_census()
        return data[-1]['population'] if data else 0
    
    def get_population_by_year(self, year: int) -> int:
        """Get tiger population for a specific year"""
        data = self.load_national_census()
        for record in data:
            if record['year'] == year:
                return record['population']
        return None
    
    def get_top_states(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get top N states by tiger population"""
        data = self.load_state_breakdown()
        return sorted(data, key=lambda x: x['population'], reverse=True)[:n]
    
    def print_summary(self):
        """Print a summary of the tiger census data"""
        print("=" * 60)
        print("INDIA TIGER CENSUS DATA SUMMARY")
        print("=" * 60)
        
        # National trend
        national_data = self.load_national_census()
        print("\nNational Tiger Population Trend:")
        print("-" * 60)
        for record in national_data:
            change_str = f"+{record['change_from_previous']}" if record['change_from_previous'] else "N/A"
            print(f"{record['year']}: {record['population']:,} tigers ({change_str})")
        
        # Latest count
        latest = national_data[-1]
        print(f"\nLatest Census ({latest['year']}): {latest['population']:,} tigers")
        print(f"Growth since 2006: +{latest['population'] - national_data[0]['population']:,} tigers")
        print(f"Growth rate: +{((latest['population'] / national_data[0]['population']) - 1) * 100:.1f}%")
        
        # Top states
        print("\n\nTop 5 States by Tiger Population (2022):")
        print("-" * 60)
        top_states = self.get_top_states(5)
        for state in top_states:
            print(f"{state['rank']}. {state['state']}: {state['population']} tigers ({state['percent_of_total']}%)")
        
        # Regional summary
        complete_data = self.load_complete_dataset()
        print("\n\nRegional Distribution (2022):")
        print("-" * 60)
        for region, population in complete_data['regional_summary_2022'].items():
            print(f"{region}: {population} tigers")
        
        print("\n" + "=" * 60)


def main():
    """Example usage of the TigerCensusDataLoader"""
    
    # Initialize loader
    loader = TigerCensusDataLoader()
    
    # Print summary
    loader.print_summary()
    
    # Example: Query specific data
    print("\n\nExample Queries:")
    print("-" * 60)
    print(f"Latest population: {loader.get_latest_population():,} tigers")
    print(f"Population in 2010: {loader.get_population_by_year(2010):,} tigers")
    print(f"Population in 2018: {loader.get_population_by_year(2018):,} tigers")


if __name__ == "__main__":
    main()

