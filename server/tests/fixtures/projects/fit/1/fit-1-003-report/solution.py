def main(n=None):
    import json
    import sys

    n = int(sys.argv[1]) if n is None else n
    print("fitted")
    print(json.dumps({"slope": fit(n)}))
