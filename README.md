Based on my learnings from Ruslan Spivak's blog (https://ruslanspivak.com/lsbasi-part1/) and Allison Kaptur's blogpost about the Bytecode project she contributed to (http://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html).

# A toy compiler, written in Python
* Lexes
* Parses (generates abstract syntax tree
* Does semantic analysis
* Generates scoped symbol tables
* Generates assembly-like instructions
* Runs the assembly-like instructions. 

Currently does simple arithmetic, prints values, variable and function declarations, some type checking, scope setting.

### Dependencies
None but for Python.

### Compile a sample text
You can run the below sample script by cloning this repo, cd'ing into it, and then running `python compile_sample_text.py`.


#### Sample text
  ```var x, y, z : int;

  function foo (p, q, n, m : int) {
      p = p + 5;
      q = q * 10;
      n = n - 4;
      m = m / 3;
  }

  function bar (r, s, t, u : int) {
      r = r + 5;
      s = s * 10;
      t = t - 4;
      u = u / 3;
  }

  print (3 + 3) * (3 - 3); # 0```
