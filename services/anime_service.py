import pandas as pd
import os

class AnimeService:
    def repeat_anime_name(self, anime_name: str, repetitions: int = 10) -> list[str]:
        """
        Repeats an anime name a specified number of times
        
        Args:
            anime_name: The name of the anime to repeat
            repetitions: Number of times to repeat the name (default: 10)
            
        Returns:
            A list containing the repeated anime name
        """
        return [anime_name] * repetitions
    
    def get_anime_info(self, anime_name: str) -> dict:
        """
        Mock function to get anime information
        In a real application, this might call an external API or database
        
        Args:
            anime_name: The name of the anime to get information for
            
        Returns:
            A dictionary with mock anime information
        """
        # This is just a mock - in a real app you'd fetch real data
        return {
            "name": anime_name,
            "genres": ["Action", "Adventure"],
            "episodes": 24,
            "rating": 4.5
        }
    def recommend_anime(self, anime_names: list[str], top_n: int = 10) -> list[str]:
        """
        Recommends similar anime based on input anime names
        
        Args:
            anime_names: List of anime names to base recommendations on
            top_n: Number of recommendations to return (default: 10)
            
        Returns:
            A list of recommended anime names
        """
        
        # Path to the similarity matrix file
        # Assuming the project structure is:
        # - Main_Folder
        #   - Backend (FastAPI project)
        #   - Model
        #      - anime_similarity.csv
        
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                     'Model', 'anime_similarity.csv')
        
        # Load similarity matrix
        try:
            ani_sim_df = pd.read_csv(file_path, index_col=0)
        except FileNotFoundError:
            return ["Error: Similarity data not found"]
            
        # Get list of all anime
        anime_list = ani_sim_df.columns.values.tolist()
        anime_scores = [(x, 0) for x in anime_list]
        
        # Calculate similarity scores
        for anime_name in anime_names:
            if (anime_name in ani_sim_df.columns):
                for i, score in enumerate(ani_sim_df[anime_name]):
                    anime_scores[i] = (anime_scores[i][0], anime_scores[i][1] + score)
            else:
                return [f"Anime '{anime_name}' not found in database"]
                
        # Sort by score and remove input anime from recommendations
        sorted_scores = sorted(anime_scores, key=lambda x: x[1], reverse=True)
        recommendations = [anime for anime, _ in sorted_scores 
                          if anime not in anime_names]
                
        return recommendations[:top_n]