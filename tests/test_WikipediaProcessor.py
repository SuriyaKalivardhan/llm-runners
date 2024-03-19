import WikipediaProcessor

def test_increment():
    assert 4 == 4

def test_wiki():
    wp = WikipediaProcessor.WikipediaProcessor()
    result = wp.get()
    assert result == 5