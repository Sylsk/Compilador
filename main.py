from parser import ejecutar_codigo

codigo = '''
x = 10;
y = 0;

print("Hello, world!");

puede_ser_pa (x > 5) {
    print("x es:", x);
} else {
    print("y es:", y);
}

while (x > 0) {
    print("x es:", x);
    x = x - 1;
}

for (z = 0; z < 5; z = z + 1) {
    print("z vale", z);
}
'''

ejecutar_codigo(codigo)
