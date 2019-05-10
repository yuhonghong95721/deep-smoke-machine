import sys
import requests
from util import *

# Get video metadata and save to a file
def main(argv):
    print("Get video metadata...")
    vm = get_video_metadata()
    
    # Save and return dataset
    file_path = "../data/metadata.json"
    check_and_create_dir(file_path)
    save_json(vm, file_path)
    
    print("Done.")

# Get video metadata from the video-labeling-tool
def get_video_metadata():
    # Read the user token, obtained from https://smoke.createlab.org/gallery.html in dashboard mode
    user_token = load_json("../data/user_token.json")["user_token"]

    # Request metadata
    url_root = "https://api.smoke.createlab.org/api/v1/"
    videos = iterative_query(url_root+"get_pos_gold_labels", user_token)
    videos += iterative_query(url_root+"get_neg_gold_labels", user_token)
    videos += iterative_query(url_root+"get_pos_labels_by_researcher", user_token)
    videos += iterative_query(url_root+"get_neg_labels_by_researcher", user_token)
 
    return videos

# Query a paginated api call iteratively until getting all the data
def iterative_query(url, user_token, page_size=1000, page_number=1):
    r = requests.post(url=url, data={"user_token": user_token, "pageSize": page_size, "pageNumber": page_number})
    r = r.json()
    total = r["total"]
    r = r["data"]
    if page_size*page_number >= total:
        return r
    else:
        return r + iterative_query(url, user_token, page_size=page_size, page_number=page_number+1)

if __name__ == "__main__":
    main(sys.argv)