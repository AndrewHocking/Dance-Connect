# Path: cloud/ai.py
import json
import time
from cdn import CDN
import random
from PIL import Image
import requests
import os
from openai import OpenAI

SECRETS = (
    os.path.join(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0])
    + "/secrets/keys.json"
)

DELAY = 15

DEBUG = False
if DEBUG:
    SIZE = "256x256"
    QUALITY = "standard"
else:
    SIZE = "1024x1024"
    QUALITY = "hd"


events = [
    {
        "title": "Latin Rhythms Fiesta",
        "description": "Get ready to salsa, bachata, and cha-cha! A lively celebration of Latin dance and music.",
        "url": "https://www.latinrhythmsfiesta.com",
        "tags": ["salsa", "bachata", "Latin", "dance"],
        "venue_name": "Casa de Sabor",
        "venue_address": "456 Salsa Avenue, Toronto, ON M4X 1Y8",
        "venue_is_mobility_aid_accessible": False,
        "accessibility_notes": "Please note that the venue has stairs and is not wheelchair accessible.",
        "min_ticket_price": 15.0,
        "max_ticket_price": 35.0,
    },
    {
        "title": "Urban Groove Showcase",
        "description": "A high-energy showcase featuring urban dance crews from across the GTA. Hip-hop, popping, and locking at its finest!",
        "url": "https://www.urbangrooveshowcase.com",
        "tags": ["hip hop", "urban", "dance", "showcase"],
        "venue_name": "Metro Arts Center",
        "venue_address": "789 Beat Street, Mississauga, ON L5R 2T3",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "The venue has accessible entrances and seating. No strobe lights during the performance.",
        "min_ticket_price": 25.0,
        "max_ticket_price": 60.0,
    },
    {
        "title": "Before You're Gone",
        "description": "“Before You’re Gone” is a poignant contemporary dance routine that captures the essence of fleeting moments and the tender ache of farewells. Performed by a solo female dancer, the piece unfolds on a dimly lit stage, where her silhouette weaves through the shadows. Her movements are a painting of love, loss, and the bittersweet beauty of final goodbyes. As the music swells, her dance intensifies, embodying the urgency and intensity of time slipping away, leaving the audience with a haunting reminder to hold close what is dear, “Before You’re Gone”.",
        "url": "https://www.beforeyouregone.com/",
        "tags": ["contemporary", "solo dancer", "emotional"],
        "venue_name": "Young Centre for the Performing Arts",
        "venue_address": "50 Tank House Lane, Toronto, ON M5A 3C4",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Strobe lighting will be used in the first 5 minutes of the performance, except for the Thursday performances. There will be dimmed lighting during all performances.",
        "min_ticket_price": 20.0,
        "max_ticket_price": 40.0,
    },
    {
        "title": "Introductory Tap Workshop",
        "description": "Passionate Argentine tango performances and social dancing. Feel the romance and intensity of this captivating dance form.",
        "url": "https://www.tangonights.com",
        "tags": ["tango", "Argentine", "dance", "passion"],
        "venue_name": "Café Milonga",
        "venue_address": "567 Embrace Avenue, Toronto, ON M6G 1X2",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "The venue is wheelchair accessible. Dimmed lighting during performances.",
        "min_ticket_price": 30.0,
        "max_ticket_price": 80.0,
    },
    # {
    #     "title": "Tango Nights",
    #     "description": "Passionate Argentine tango performances and social dancing. Feel the romance and intensity of this captivating dance form.",
    #     "url": "https://www.tangonights.com",
    #     "tags": ["tango", "Argentine", "dance", "passion"],
    #     "venue_name": "Café Milonga",
    #     "venue_address": "567 Embrace Avenue, Toronto, ON M6G 1X2",
    #     "venue_is_mobility_aid_accessible": True,
    #     "accessibility_notes": "The venue is wheelchair accessible. Dimmed lighting during performances.",
    #     "min_ticket_price": 30.0,
    #     "max_ticket_price": 80.0
    # },
    {
        "title": "Bollywood Beats Festival",
        "description": "A vibrant celebration of Bollywood dance, music, and culture. Get ready to move to the rhythm of India!",
        "url": "https://www.bollywoodbeatsfest.com",
        "tags": ["Bollywood", "Indian", "dance", "festival"],
        "venue_name": "Rangoli Pavilion",
        "venue_address": "234 Sitar Lane, Brampton, ON L6P 3H5",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible entrance on the west side of the venue. No strobes or intense flashing lights.",
        "min_ticket_price": 20.0,
        "max_ticket_price": 50.0,
    },
    {
        "title": "Contemporary Collisions",
        "description": "An experimental showcase blending contemporary dance with multimedia art. Prepare for thought-provoking performances.",
        "url": "https://www.contemporarycollisions.com",
        "tags": ["contemporary", "experimental", "dance", "art"],
        "venue_name": "Gallery X",
        "venue_address": "345 Canvas Avenue, Toronto, ON M4S 2W9",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Wheelchair ramps available. Minimal use of flashing lights.",
        "min_ticket_price": 25.0,
        "max_ticket_price": 70.0,
    },
    {
        "title": "Salsa Sunset Social",
        "description": "Dance the night away to sizzling salsa beats by the waterfront. Beginners and pros welcome!",
        "url": "https://www.salsasunset.com",
        "tags": ["salsa", "Latin", "dance", "social"],
        "venue_name": "Harbourview Pavilion",
        "venue_address": "123 Salsa Bay, Toronto, ON M5J 2T4",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible pathways to the venue. No strobe lights during the social dance.",
        "min_ticket_price": 15.0,
        "max_ticket_price": 40.0,
    },
    {
        "title": "Fusion Fireworks",
        "description": "A mesmerizing blend of classical Indian dance, contemporary movement, and fire spinning. Prepare to be amazed!",
        "url": "https://www.fusionfireworks.com",
        "tags": ["Indian dance", "contemporary", "fire spinning", "spectacle"],
        "venue_name": "Firefly Gardens",
        "venue_address": "789 Flame Avenue, Markham, ON L3R 5T2",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible pathways throughout the venue. Fire performance is outdoors.",
        "min_ticket_price": 25.0,
        "max_ticket_price": 60.0,
    },
    {
        "title": "Ballet in the Park",
        "description": "An enchanting outdoor ballet performance set against a natural backdrop. Bring a picnic blanket and enjoy the artistry.",
        "url": "https://www.balletinthepark.com",
        "tags": ["ballet", "outdoor", "nature", "performance"],
        "venue_name": "Sunset Meadow",
        "venue_address": "123 Tutu Trail, Vaughan, ON L4J 8K9",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible parking available. No sudden lighting changes during the show.",
        "min_ticket_price": 15.0,
        "max_ticket_price": 35.0,
    },
    {
        "title": "Break the Beat Battle",
        "description": "Witness jaw-dropping breakdance battles as crews battle it out for supremacy. Who will break the beat?",
        "url": "https://www.breakthebeatbattle.com",
        "tags": ["breakdance", "b-boy", "competition", "street dance"],
        "venue_name": "Concrete Arena",
        "venue_address": "456 Break Street, Scarborough, ON M1B 2C3",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible seating available. No intense strobes during battles.",
        "min_ticket_price": 10.0,
        "max_ticket_price": 25.0,
    },
    {
        "title": "Flamenco Fiesta",
        "description": "Passionate flamenco performances accompanied by live guitar music. Olé!",
        "url": "https://www.flamencofiesta.com",
        "tags": ["flamenco", "Spanish", "dance", "passion"],
        "venue_name": "Casa del Flamenco",
        "venue_address": "234 Sevillana Street, Richmond Hill, ON L4S 1T5",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Wheelchair ramps at the entrance. No sudden light changes during performances.",
        "min_ticket_price": 30.0,
        "max_ticket_price": 70.0,
    },
    {
        "title": "Rhythm Revival",
        "description": "A soulful evening of tap dance, live jazz, and spoken word. Celebrate the art of rhythm!",
        "url": "https://www.rhythmrevival.com",
        "tags": ["tap", "jazz", "spoken word", "performance"],
        "venue_name": "Harmony Hall",
        "venue_address": "789 Sync Street, Etobicoke, ON M9B 2T1",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible seating available. No sudden light changes during performances.",
        "min_ticket_price": 20.0,
        "max_ticket_price": 55.0,
    },
]

users = [
    {
        "display_name": "Grace Turner",
        "username": "grace123",
        "email": "grace.turner@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Passionate ballet dancer and choreographer. Loves expressing emotions through movement.",
        "tags": ["ballet", "dancer", "choreographer"],
    },
    {
        "display_name": "Alex Rivera",
        "username": "alex_r",
        "email": "alex.rivera@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Hip-hop enthusiast. Always ready to break it down on the dance floor.",
        "tags": ["hip hop", "dancer"],
    },
    {
        "display_name": "Luna Vega",
        "username": "lunavega",
        "email": "luna.vega@example.com",
        "password": "password",
        "pronouns": "they/them",
        "bio": "Contemporary dancer with a flair for storytelling. Loves experimenting with movement.",
        "tags": ["contemporary", "dancer"],
    },
    {
        "display_name": "Sophia Lee",
        "username": "sophia_dance",
        "email": "sophia.lee@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Classical ballet dancer with a passion for pointe work. Loves performing in story ballets.",
        "tags": ["ballet", "dancer", "choreographer"],
    },
    {
        "display_name": "Max Vega",
        "username": "maxvega",
        "email": "max.vega@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Versatile dancer skilled in hip-hop, contemporary, and salsa. Choreographs high-energy routines.",
        "tags": ["hip hop", "contemporary", "salsa", "dancer", "choreographer"],
    },
    {
        "display_name": "Elena Rodriguez",
        "username": "elenarod",
        "email": "elena.rodriguez@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Latin ballroom specialist. Enjoys partnering and competing in international dance events.",
        "tags": ["ballroom", "dancer", "competitor"],
    },
    {
        "display_name": "Isabella Rodriguez",
        "username": "izzyrod",
        "email": "isabella.rodriguez@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Isabella Rodriguez, a trailblazing force in the dance industry, has dedicated her life to transforming movement into captivating narratives. Known for her ability to fuse different dance styles and evoke powerful emotions through movement, Isabella continues to push the boundaries of artistic expression. With a repertoire of breathtaking performances and a commitment to pushing the art form forward, Isabella Rodriguez stands as a beacon of innovation in the world of dance.",
        "tags": ["choreographer", "artistic director", "contemporary", "indie"],
    },
    {
        "display_name": "Oliver Grant",
        "username": "oliver_g",
        "email": "oliver.grant@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Jazz funk enthusiast. Loves grooving to funky beats and creating dynamic choreography.",
        "tags": ["jazz funk", "dancer", "choreographer"],
    },
    {
        "display_name": "Maya Patel",
        "username": "mayadance",
        "email": "maya.patel@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Indian classical dancer (Bharatanatyam). Passionate about preserving cultural heritage through dance.",
        "tags": ["Bharatanatyam", "dancer", "cultural"],
    },
    {
        "display_name": "Lucas Martin",
        "username": "lucas_m",
        "email": "lucas.martin@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Tap dancer extraordinaire. Rhythmic footwork and syncopation are my jam!",
        "tags": ["tap", "dancer"],
    },
    {
        "display_name": "Isabella Wong",
        "username": "isabellaw",
        "email": "isabella.wong@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Contemporary flow artist. Expresses emotions through fluid movement and improvisation.",
        "tags": ["contemporary", "dancer"],
    },
    {
        "display_name": "David Foster",
        "username": "davidf",
        "email": "david.foster@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Experienced stage manager. Ensures seamless performances behind the scenes.",
        "tags": ["stage manager", "production"],
    },
    {
        "display_name": "Nina Chen",
        "username": "ninac",
        "email": "nina.chen@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Dance journalist and writer. Chronicles the magic of movement through words.",
        "tags": ["writer", "journalist", "dance"],
    },
    {
        "display_name": "Carlos Ramirez",
        "username": "carlosr",
        "email": "carlos.ramirez@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Salsa instructor and performer. Spreads the joy of Latin dance.",
        "tags": ["salsa", "instructor", "performer"],
    },
    {
        "display_name": "Emily Parker",
        "username": "emily_dance",
        "email": "emily.parker@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Versatile dancer trained in jazz, contemporary, and ballroom. Loves performing on stage.",
        "tags": ["jazz", "contemporary", "ballroom", "dancer", "performer"],
    },
    {
        "display_name": "Leo Kim",
        "username": "leok",
        "email": "leo.kim@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "K-pop dance enthusiast. Choreographs dynamic routines inspired by K-pop idols.",
        "tags": ["K-pop", "choreographer", "dancer"],
    },
    {
        "display_name": "Aria Patel",
        "username": "ariadance",
        "email": "aria.patel@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Latin fusion dancer. Combines salsa, bachata, and tango for a unique style.",
        "tags": ["salsa", "bachata", "tango", "fusion", "dancer"],
    },
    {
        "display_name": "Evan Foster",
        "username": "evanf",
        "email": "evan.foster@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Lighting and sound technician. Ensures dazzling performances with perfect cues.",
        "tags": ["stage manager", "technician", "production"],
    },
    {
        "display_name": "Zara Liu",
        "username": "zaral",
        "email": "zara.liu@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Bollywood dance lover. Spreads joy through vibrant and energetic routines.",
        "tags": ["Bollywood", "dancer", "enthusiast"],
    },
    {
        "display_name": "Samuel Rodriguez",
        "username": "samuelr",
        "email": "samuel.rodriguez@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Breakdancer (b-boy). Pops, locks, and spins to the beat!",
        "tags": ["breakdance", "b-boy", "dancer"],
    },
    {
        "display_name": "Lila Chen",
        "username": "lilac",
        "email": "lila.chen@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Experimental movement artist. Pushes boundaries and challenges norms.",
        "tags": ["experimental", "movement", "artist"],
    },
    {
        "display_name": "Daniel Wong",
        "username": "danielw",
        "email": "daniel.wong@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Contemporary ballet dancer. Melds classical technique with modern expression.",
        "tags": ["contemporary ballet", "dancer"],
    },
    {
        "display_name": "Mia Johnson",
        "username": "miaj",
        "email": "mia.johnson@example.com",
        "password": "password",
        "pronouns": "she/her",
        "bio": "Urban dance advocate. Empowers youth through hip-hop workshops.",
        "tags": ["hip hop", "urban", "advocate", "teacher"],
    },
    {
        "display_name": "Oscar Morales",
        "username": "oscarm",
        "email": "oscar.morales@example.com",
        "password": "password",
        "pronouns": "he/him",
        "bio": "Salsa social dancer. Spins partners with flair and infectious energy.",
        "tags": ["salsa", "social dancer", "enthusiast"],
    },
]


def profilePics():
    try:
        with open(SECRETS, "r") as file:
            data = json.load(file)
            api_key = data["cloudflare"]["api_key"]
            file.close()
    except Exception:
        print("ERROR: Failed to read keys from secrets folder")

    # print(api_key)
    client = OpenAI(api_key=api_key)
    client.api_key = api_key

    random.seed()

    # set a directory to save DALL·E images to
    # image_dir_name = "temp"
    # image_dir = os.path.join(os.curdir, image_dir_name)
    # image_dir = "./wesbsite/cloud/temp/"

    image_dir = os.path.join(os.path.dirname(__file__)) + "/aiPictures/"

    # # create the directory if it doesn't yet exist
    # if not os.path.isdir(image_dir):
    #     os.mkdir(image_dir)
    newlist = []
    cdn = CDN()
    count = 1
    for user in users:
        print(f"doing: {count}/{len(users)}")
        count += 1
        time.sleep(DELAY)
        # for a person with the following characteristics: {user['bio']}"
        prompt = (
            f"social media profile picture of {user['display_name']} aged between 20-45"
        )
        generation_response = client.images.generate(
            prompt=prompt, n=1, size=SIZE, quality=QUALITY
        )
        # print(generation_response.data[0].url)
        # variation_urls = [datum["url"]
        #                   for datum in generation_response.data]  # extract URLs

        variation_images = requests.get(
            generation_response.data[0].url
        )  # download images

        # create name
        variation_image_name = f"DEBUG_PROFILE_PICTURE_{user['display_name']}_{str(random.randint(0, 99999))}.png"

        variation_image_filepaths = os.path.join(image_dir, variation_image_name)

        with open(variation_image_filepaths, "wb") as image_file:  # open the file
            # write the image to the file
            image_file.write(variation_images.content)

        # with open("./temp/", "wb") as image_file:  # open the file
        #     image_file.write(variation_images)  # write the image to the file

        output = cdn.upload(variation_image_filepaths)
        if len(output["errors"]) > 0:
            print(f"Error uploading image: {output}")
        else:
            user["profile_picture_url"] = output["result"]["variants"][0]
            user["profile_picture_id"] = output["result"]["id"]
            newlist.append(user)

    with open("./website/cloud/demoPeople.txt", "w") as file:
        file.write(str(newlist))


def eventPics():
    """
    "title": "Rhythm Revival",
        "description": "A soulful evening of tap dance, live jazz, and spoken word. Celebrate the art of rhythm!",
        "url": "https://www.rhythmrevival.com",
        "tags": ["tap", "jazz", "spoken word", "performance"],
        "venue_name": "Harmony Hall",
        "venue_address": "789 Sync Street, Etobicoke, ON M9B 2T1",
        "venue_is_mobility_aid_accessible": True,
        "accessibility_notes": "Accessible seating available. No sudden light changes during performances.",
        "min_ticket_price": 20.0,
        "max_ticket_price": 55.0
    },
    """
    try:
        with open(SECRETS, "r") as file:
            data = json.load(file)
            api_key = data["cloudflare"]["api_key"]
            file.close()
    except Exception:
        print("ERROR: Failed to read keys from secrets folder")

    client = OpenAI(api_key=api_key)
    client.api_key = api_key

    random.seed()

    # set a directory to save DALL·E images to
    # image_dir_name = "temp"
    # image_dir = os.path.join(os.curdir, image_dir_name)
    # image_dir = "./wesbsite/cloud/temp/"

    image_dir = os.path.join(os.path.dirname(__file__)) + "/aiPictures/"

    # # create the directory if it doesn't yet exist
    # if not os.path.isdir(image_dir):
    #     os.mkdir(image_dir)
    newlist = []
    cdn = CDN()
    count = 1
    for event in events:
        print(f"doing: {count}/{len(events)}")
        count += 1
        time.sleep(DELAY)
        prompt = f"show a picture of the event for {event['title']} with the following characteristics: {event['description']}"
        generation_response = client.images.generate(
            prompt=prompt, n=1, size=SIZE, quality=QUALITY
        )
        # print(generation_response.data[0].url)
        # variation_urls = [datum["url"]
        #                   for datum in generation_response.data]  # extract URLs

        variation_images = requests.get(
            generation_response.data[0].url
        )  # download images

        # create name
        variation_image_name = (
            f"DEBUG_EVENT_PICTURE_{event['title']}_{str(random.randint(0, 99999))}.png"
        )

        variation_image_filepaths = os.path.join(image_dir, variation_image_name)

        with open(variation_image_filepaths, "wb") as image_file:  # open the file
            # write the image to the file
            image_file.write(variation_images.content)

        # with open("./temp/", "wb") as image_file:  # open the file
        #     image_file.write(variation_images)  # write the image to the file

        output = cdn.upload(variation_image_filepaths)
        if len(output["errors"]) > 0:
            print(f"Error uploading image: {output}")
        else:
            event["image_picture_url"] = output["result"]["variants"][0]
            event["image_picture_id"] = output["result"]["id"]
            newlist.append(event)

    with open("./website/cloud/demoEvents.txt", "w") as file:
        file.write(str(newlist))


# profile_picture_url="",
#      profile_picture_id="",
#
# size="1024x1024"
# size="256x256"

# save the images


if __name__ == "__main__":
    # profilePics()
    eventPics()
    # try:
    #     with open(SECRETS, "r") as file:
    #         data = json.load(file)
    #         api_key = data["cloudflare"]["api_key"]
    #         file.close()
    # except Exception:
    #     print("ERROR: Failed to read keys from secrets folder")
    # print(api_key)
    # Open the file in write mode ('w')
    # with open('./website/cloud/demoPeople.txt', 'w') as file:
    #     file.write(str(users))
    # print(len(users))
    # image_dir = os.path.join(
    #     os.path.dirname(__file__)) + "/temp"
    # print(image_dir)
    # main()


"""    
# save the image
generated_image_name = str(random.randint(0,99999)) + "__" + PROMPT + ".png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)

    """
