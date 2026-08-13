from curl_cffi import requests

url = "https://api.themoviedb.org/3/search/movie"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZjdjZThiNDVmMGZiNWRhOTExNjY0MzAyNTk0YWUyNSIsIm5iZiI6MTc4NjUzMzIxMy4wMjQ5OTk5LCJzdWIiOiI2YTdjNTU1ZDk2OGFkYjlkYzRjN2FhMjciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.Rlawz_g78EQkaQQIOR-g871pF2sAnB5pnevQlbbor_g",
    "accept": "application/json"
}

params = {
    "query": "Titanic"
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    impersonate="chrome"
)

print("Status:", response.status_code)
print(response.text[:500])