from functools import lru_cache


@lru_cache(maxsize=4096)
def levenshtein_distance(s: str, t: str) -> int:
    s = s.upper()
    t = t.upper()
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[0] == t[0]:
        return levenshtein_distance(s[1:], t[1:])

    l1 = levenshtein_distance(s, t[1:])
    l2 = levenshtein_distance(s[1:], t)
    l3 = levenshtein_distance(s[1:], t[1:])
    return 1 + min(l1, l2, l3)
