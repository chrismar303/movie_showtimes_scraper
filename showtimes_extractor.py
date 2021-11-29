import time
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class MovieShowtimeExtractor:
    DRIVER_PATH = config.DRIVER_PATH
    STARTING_PAGE = 'https://www.amctheatres.com/movie-theatres'

    def __init__(self, zip_code):
        self.zip_code = zip_code
        self.movie_showtimes_data = []
        self.browser = self.__init_selenium__()

    def __init_selenium__(self):
        return webdriver.Chrome(MovieShowtimeExtractor.DRIVER_PATH)

    def open_browser(self):
        self.browser.get(MovieShowtimeExtractor.STARTING_PAGE)

    def enter_location(self):
        theater_location_form = self.browser.find_element_by_css_selector('.TheatreSearchField-form > input')
        time.sleep(2)

        theater_location_form.send_keys(self.zip_code, Keys.ENTER)
        time.sleep(3)

    def select_closest_theater(self):
        showtimes_button = self.browser.find_element_by_css_selector('.TheatreFinder-links > a')
        showtimes_button.click()
        time.sleep(5)

    def extract_data(self):
        movies = self.__get_all_movies__()
        for movie in movies:
            title, description = self.__extract_header_info__(movie)
            showtimes, format_type = self.__extract_showtimes_data__(movie)
            self.movie_showtimes_data.append(Movie(title, description, showtimes))

    def __extract_header_info__(self, movie):
        movie_header = movie.find_element_by_css_selector('.MovieTitleHeader-title')
        description_link = movie_header.get_attribute('href')
        movie_title = movie_header.find_element_by_tag_name('h2').text
        return movie_title, description_link

    def __extract_showtimes_data__(self, movie):
        format_type = self.__get_format_info__(movie)

        showtimes = []
        showtimes_list = movie.find_elements_by_css_selector('.Showtime')
        for showtime_container in showtimes_list:
            showtime, showtime_link = self.__get_showtime_and_link__(showtime_container)
            showtimes.append({'time': showtime, 'purchase_link': showtime_link})

        return showtimes, format_type

    def __get_format_info__(self, movie):
        format_type = movie.find_element_by_css_selector('.Showtimes-Section--PremiumFormat-Heading-Title > h4')
        return format_type.text

    def __get_showtime_and_link__(self, showtime_container):
        showtime_link = showtime_container.find_element_by_tag_name('a')
        showtime = showtime_link.text
        showtime_link = showtime_link.get_attribute('href')
        return showtime, showtime_link

    def __get_all_movies__(self):
        movies_list = self.browser.find_elements_by_class_name('ShowtimesByTheatre-film')
        return movies_list

    def close_popup(self):
        try:
            popup = self.browser.find_element_by_css_selector('.onboarding-tour-modal__controls button')
            popup.click()
        except:
            print('no popup')

    def save_results(self):
        with open(f'Movies.txt', 'w') as file:
            for movie in self.movie_showtimes_data:
                file.write(f'{movie.title}\n')
                file.write(f'description: {movie.description_url}\n')
                for showtime in movie.showtimes:
                    file.write(f'Time: {showtime["time"]} \n {showtime["purchase_link"]}\n')
                file.write('\n=============================================================\n')


class Movie:
    def __init__(self, title, description_url, showtimes):
        self.title = title
        self.description_url = description_url
        self.showtimes = showtimes

