from scraper import main_scraper
import fire
import wikipediaapi

def scrape_data(movie_name:str):
    # if save_name=="":save_name="_".join(movie_name.split(" "))
    wikipedia_module = wikipediaapi.Wikipedia('ADTProject (athecolab@gmail.com)', 'en')
    return main_scraper(movie_name=movie_name,wikipedia_module=wikipedia_module)

if __name__ == "__main__":
    fire.Fire(scrape_data)