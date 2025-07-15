import collections
import math


def _get_frequencies(words: list[str]) -> dict[str, int]:
    """
    Given a list of words, returns a dictionary of each word mapped to its count in the list.
    :param words: List of words to count.
    :return: Dictionary from word to its count.
    """
    freqs = dict()
    counts = dict(collections.Counter(words))
    n = len(words)

    for word in counts.keys():
        freqs[word] = counts[word] / n

    return freqs


class Page:
    """
    This class represents a webpage and helps with word frequency calculations.
    """
    def __init__(self, title: str, url: str, text: str) -> None:
        """
        Creates new page with title, url, and text to process.
        :param title: Title of webpage
        :param url: Url of webpage
        :param text: Text from page
        """
        self._title: str = title
        self._url: str = url
        self._word_frequencies: dict[str: int] = _get_frequencies(text.lower().split())

    def get_frequency(self, word) -> int:
        """
        Given a word, returns the count of that word in the page.
        :param word: Word to get count of
        :return: Word count
        """
        if word in self._word_frequencies:
            return self._word_frequencies[word.lower()]
        else:
            return 0

    def get_words(self) -> set[str]:
        """
        :return: Unique words in the page.
        """
        return set(self._word_frequencies.keys())

    def get_title(self) -> str:
        """
        :return: Page title
        """
        return self._title

    def get_url(self) -> str:
        """
        :return: Page url
        """
        return self._url


class SearchEngine:
    """
    Search Engine used for ranking pages based on searches
    """
    def __init__(self, pages: list[Page]) -> None:
        """
        Creates new search engine containing the given pages.
        :param pages: List of pages in the search engine
        """
        self._pages: list[Page] = pages # list of pages
        self._inverted_index: dict[str, list[Page]] = dict() # dict from word to pages containing word

        for page in pages:
            words = page.get_words()
            for word in words:
                if word in self._inverted_index:
                    self._inverted_index[word].append(page)
                else:
                    self._inverted_index[word] = [page]

    def _get_idf(self, word: str) -> float:
        """
        Given a word, returns the idf score of the word.
        :param word: Word to get the score of
        :return: idf score of the word
        """
        word = word.lower()
        n = len(self._pages)
        word_count = len(self._inverted_index[word])

        if word_count == 0:
            return 0
        else:
            return math.log(n / word_count)

    def search(self, query: str) -> list[tuple[str, str]]:
        """
        Given a query, returns a list of page titles and urls ordered
        by most relevant to least relevant to the query.
        :param query: Search query for pages
        :return: Pages ordered by most relevant to query
        """
        page_scores = dict()
        for word in query.lower().split():
            if word in self._inverted_index.keys():
                for page in self._inverted_index[word]:
                    freq = page.get_frequency(word)
                    score = freq * self._get_idf(word)
                    page_info = (page.get_title(), page.get_url())

                    if page_info in page_scores:
                        page_scores[page_info] = score + page_scores[page_info]
                    else:
                        page_scores[page_info] = score

        out = list(page_scores.keys())
        return sorted(out, key=lambda info: page_scores[info], reverse=True)

