from utils.google_api import GoogleSearch
google = GoogleSearch()

if __name__ == "__main__":    
    query = 'ai là người giàu nhất Việt Nam'
        
    data = google.search(query)

    for topic in data:
        print(topic)