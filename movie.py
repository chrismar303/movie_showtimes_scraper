import sys
from util import get_zip_code
from showtimes_extractor import MovieShowtimeExtractor


def main():
    zip_code = get_zip_code(sys.argv)
    extractor = MovieShowtimeExtractor(zip_code)
    extractor.open_browser()
    extractor.close_popup()
    extractor.enter_location()
    extractor.select_closest_theater()
    extractor.extract_data()
    extractor.save_results()


if __name__ == '__main__':
    main()
