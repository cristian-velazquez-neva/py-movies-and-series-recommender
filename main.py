import requests
import random

def get_data(url, headers, params=None):
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_genres(url, headers, content):
    url = f"{url}/genre/{content}/list"
    return get_data(url, headers)

def get_elements_by_genre(url, headers, content, genre):
    url = f"{url}/discover/{content}"
    params = {
        "with_genres": genre
    }
    return get_data(url, headers, params)

def search_actor(url, headers, actor):
    url = f"{url}/search/person"
    params = {
        "query": actor
    }
    return get_data(url, headers, params)

def get_elements_by_actor(url, headers, content, actor):
    url = f"{url}/discover/{content}"
    params = {
        "with_actor": actor
    }
    return get_data(url, headers, params)

if __name__ == "__main__":
    SECRET_KEY = open("api_key", "r").read()
    url = "https://api.themoviedb.org/3"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {SECRET_KEY}"
    }
    
    while True:
        choice = int(input("What Would You Like to See?\n1. Movie\n2. Serie\n"))
        option = int(input("Select a Filter.\n1. Actor\n2. Genre\n"))
        content = None
        elements = None
        
        if choice == 1:
            content = "movie"
        elif choice == 2:
            content = "tv"
            
        if option == 1:
            actor_name = input("Enter the actor you want to see: ")
            actor_search = search_actor(url, headers, actor_name)
            actor_id = actor_search["results"][0]["id"]
            elements = get_elements_by_actor(url, headers, content, actor_id)
        elif option == 2:
            genres = get_genres(url, headers, content)
            for genre in genres["genres"]:
                print(f"{genre["id"]}. {genre["name"]}")
                
            genre = int(input("Select a Genre: "))
            elements = get_elements_by_genre(url, headers, content, genre)
            
        while True:
            element = random.choice(elements['results'])
            if content == "movie":
                print(f'Recommended: {element["title"]}')
            elif content == "tv":
                print(f'Recommended: {element["name"]}')

            repeat = input("Show another (y/n)? ")
            if repeat.lower() != "y":
                break

        repeat = input("Do you want to return to the menu (y/n)? ")
        if repeat.lower() != "y":
            break