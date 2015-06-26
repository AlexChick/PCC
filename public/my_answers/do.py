from pyjs import translator

import tempfile, os
tmp = tempfile.mkdtemp()

mymodule1 = os.path.join(tmp, 'mymodule1.py')
out_file = os.path.join(tmp, 'mymodule1.js')
f = file(mymodule1, 'w')
f.write("""
    def main():
        print 1
    if __name__=='__main__':
        main()
    """)
f.close()







out_file = os.path.join(tmp, 'imports.js')
imports = os.path.join(tmp, 'imports.py')
f = file(imports, 'w')
f.write("""
    import a
    from x.z import y, p as pp
    import a.b
    a.b.something()
    import a
    import a as a_foo
    a.something()
    a = 0
    a += 1
    bb = 0
    from a.b import c
    c()
    a = 42
    def main():
        import a.b
        a.b.something()
        a = 1
        import z as x
        x()
        from x.z import y, p as pp
    """)
f.close()

translator.translate([imports], out_file,
                         debug=False,
                         print_statements = True,
                         function_argument_checking=True,
                         attribute_checking=True,
                         source_tracking=False,
                         line_tracking=False,
                         store_source=False)
(['a', 'x.z.y', 'x', 'x.z', 'x.z.p', 'a.b', 'a.b.c', 'z'], set([]))

print(file(outfile).read())




