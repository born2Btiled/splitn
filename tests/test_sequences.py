from splitn import sequences

def test_random_sequence_return_type():
    assert isinstance(sequences.random_sequence(r'\d[a-d]{4,7}'), str)

def test_random_sequence_sequence_length():
    assert len(sequences.random_sequence(r'a{4}')) == 4
