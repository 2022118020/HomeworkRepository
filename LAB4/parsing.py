import pandas as pd
import json

# Load CSV
file_path = 'movies_metadata.csv'
movies_df = pd.read_csv(file_path)

# Convert 'genres' from string to list of genre names
import ast
def parse_genres(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)
        return [g['name'] for g in genres_list]
    except:
        return []

# Select top 20 movies for display
movies = []
for _, row in movies_df.head(20).iterrows():
    movies.append({
        "title": row['title'],
        "overview": row['overview'] if pd.notna(row['overview']) else "No description available.",
        "genres": parse_genres(row['genres']),
        "release_date": row['release_date'] if pd.notna(row['release_date']) else "Unknown",
        "runtime": int(row['runtime']) if pd.notna(row['runtime']) else "Unknown",
        "vote_average": float(row['vote_average']) if pd.notna(row['vote_average']) else "N/A"
    })

# Create JSON structure
movies_json = {"movies": movies}

# Save to product.json
output_path = 'movies.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(movies_json, f, ensure_ascii=False, indent=4)

print(f"JSON file saved to {output_path}")
