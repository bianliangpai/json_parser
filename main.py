import os, sys
local_dir = os.path.dirname(os.path.abspath(__file__))

try:
    old_PYTHONPATH = os.environ["PYTHONPATH"]
except:
    old_PYTHONPATH = ""
# 'nt' means windows
if os.name == 'nt':
    os.environ["PYTHONPATH"] = "{};{}".format(local_dir, old_PYTHONPATH)
else:
    os.environ["PYTHONPATH"] = "{}:{}".format(local_dir, old_PYTHONPATH)

from json_parser.lex    import Lexer
from json_parser.syntax import Syntaxer


def get_content(filename):
    with open(filename, 'r') as j:
        return j.read()

def main():
    source_file = "{}/sample.json".format(local_dir)
    if sys.argv == 2:
        source_file = sys.argv[1]

    content = get_content(source_file)
    lexer = Lexer(content)
    # print(str(lexer))

    syntaxer = Syntaxer(lexer)
    result = syntaxer.run()
    print(str(result))

if __name__ == '__main__':
    main()