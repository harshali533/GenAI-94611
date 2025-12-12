<<<<<<< HEAD
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
=======
from post_api import get_posts
from weather import get_weather

def line():
    print("-" * 40)

def main():
    line()
    print("WeatherApp")
    line()
    print("1) Fetch Posts")
    print("2) Get Weather Info")
    print("3) Exit")
    line()

    choice = input("Enter your choice: ")

    if choice == "1":
        posts = get_posts()
        print("\nTotal posts:", len(posts))
        print("First post:", posts[0]["title"])

    elif choice == "2":
        city = input("Enter city: ")
        res = get_weather(city)

        print("status:", res.status_code)

        if res.status_code == 200:
            data = res.json()
            print("City:", data["name"])
            print("Temperature:", data["main"]["temp"], "°C")
            print("Humidity:", data["main"]["humidity"], "%")
            print("Description:", data["weather"][0]["description"])
        else:
            print("Error:", res.json())

    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
>>>>>>> 8977d95704341f6237b63e05b6d9eadc6e4a5bf5
