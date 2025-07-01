import collections
import math

def _get_frequencies(words):
    freqs = dict()
    counts = dict(collections.Counter(words))
    n = len(words)

    for word in counts.keys():
        freqs[word] = counts[word] / n

    return freqs


class Page:
    def __init__(self, title, url, text):
        self._title = title
        self._url = url
        self._words = text.lower().split()
        self._word_frequencies = _get_frequencies(self._words)

    def get_frequency(self, word):
        if word in self._word_frequencies:
            return self._word_frequencies[word.lower()]
        else:
            return 0

    def get_words(self):
        return self._word_frequencies.keys()

    def get_title(self):
        return self._title

    def get_url(self):
        return self._url


class SearchEngine:
    def __init__(self, pages):
        """
        :param pages: List of pages in the search engine
        """
        self._pages = pages # list of pages
        self._inverted_index = dict() # dict from word to documents containing word

        for page in pages:
            words = page.get_words()
            for word in words:
                if word in self._inverted_index:
                    self._inverted_index[word].append(page)
                else:
                    self._inverted_index[word] = [page]

    def _get_idf(self, word):
        word = word.lower()
        n = len(self._pages)
        word_count = len(self._inverted_index[word])

        if word_count == 0:
            return 0
        else:
            return math.log(n / word_count)

    def search(self, query):
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

