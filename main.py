from scraper import main_scraper
import fire

def scrape_data(movie_name:str):
    # if save_name=="":save_name="_".join(movie_name.split(" "))
    return main_scraper(movie_name=movie_name)

if __name__ == "__main__":
    fire.Fire(scrape_data)