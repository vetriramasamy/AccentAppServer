from server.rewrite import rewrite_to_american_english


def test_replaces_known_phrases_and_capitalizes():
    out = rewrite_to_american_english("i'm name is john")
    assert out == "My name is john"


def test_handles_sentences_and_punctuation():
    out = rewrite_to_american_english("I am having doubt about this.")
    assert out == "I have a question about this."


def test_returns_capitalized_text_when_no_corrections():
    assert rewrite_to_american_english("HELLO WORLD") == "Hello world"
    assert rewrite_to_american_english("i'm named john") == "I'm named john"
