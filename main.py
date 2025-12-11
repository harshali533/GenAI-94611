import arithmetic as arith
import geomety as geo

print("hello world! 🌸")

arith.add(5,5)

length = float(input("Enter length: "))
width = float(input("Enter width: "))

area = geo.rectangle_area(length, width)
perimeter = geo.rectangle_perimeter(length, width)

print("Area of rectangle =", area)
print("Perimeter of rectangle =", perimeter)
