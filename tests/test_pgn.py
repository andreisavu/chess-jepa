
from chess_jepa.tokenizer import encode
from chess_jepa.pgn import extract_training_samples

def test_simple_pgn():
    pgn = """[Event "Game on 2024.01.23 20:39:12 UTC | Coach Moves: 5"]
[Date "2024.01.23"]
[Result "0-1"]

1. e4 e5 2. Nc3 Nf6 3. d4 exd4 4. Nb5 c5 5. Qd3 d5 6. Qg3 Nxe4 7. Nc7+ Kd7 
8. Bb5+ Nc6 9. Qe5 Nd6 10. Qxd5 Qxc7 11. c3 Kd8 12. Be2 Be6 13. Qxc5 Ne4 14. Bf4 Nxc5 
15. Bxc7+ Kxc7 16. f3 dxc3 17. O-O-O cxb2+ 18. Kxb2 Na4+ 19. Kb1 Bc5 20. Rd2 Rad8 
21. Rxd8 Rxd8 22. g3 Bf5+ 23. Bd3 Rxd3 24. Kc2 Rd4+ 25. Kb3 Na5# 0-1
"""

    data = []
    for sample in extract_training_samples(pgn, window_size=5):
        data.append(encode(sample))
        print(len(encode(sample)))

    assert len(data) == 55
    assert len(data[0]) == 84 # tokens for each sample
    
    # verify that all the samples have the same length
    assert len(set(len(sample) for sample in data)) == 1