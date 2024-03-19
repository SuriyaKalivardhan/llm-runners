import WikipediaProcessor

def test_wiki_response():
    wp = WikipediaProcessor.WikipediaProcessor()
    resp = wp.get_input(10)
    assert(len(resp.Prompt) == 10)
    assert(len(resp.Expected_Generation) > 0)
